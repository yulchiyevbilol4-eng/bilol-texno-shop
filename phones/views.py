import os
import json
import logging
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Phone, Order

# Xatoliklarni terminalda kuzatish uchun logging
logger = logging.getLogger(__name__)

# =============================================================================
# 🏠 ASOSIY SAHIFALAR
# =============================================================================

def home(request):
    query = request.GET.get('q', '').strip()
    if query:
        phones = Phone.objects.filter(name__icontains=query).order_by('-id')
    else:
        phones = Phone.objects.all().order_by('-id')
    return render(request, 'index.html', {'phones': phones})

def phone_detail(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    related = Phone.objects.exclude(pk=pk).filter(brand=phone.brand)[:4] if phone.brand else []
    return render(request, 'phone_detail.html', {'phone': phone, 'related': related})

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

# =============================================================================
# 📂 KATALOG (Filtrlash)
# =============================================================================

def catalog(request):
    phones = Phone.objects.all().order_by('-id')
    
    brand_filter = request.GET.get('brand', '').strip()
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    search_query = request.GET.get('q', '').strip()
    
    if search_query:
        phones = phones.filter(name__icontains=search_query)
        
    if brand_filter:
        phones = phones.filter(brand__iexact=brand_filter)
        
    if min_price.isdigit():
        phones = phones.filter(price__gte=int(min_price))
            
    if max_price.isdigit():
        phones = phones.filter(price__lte=int(max_price))
    
    brands_list = Phone.objects.values_list('brand', flat=True).distinct().order_by('brand')
    
    context = {
        'phones': phones,
        'brands': brands_list,
        'selected_brand': brand_filter,
        'min_price': min_price,
        'max_price': max_price,
        'search_query': search_query,
        'total_count': phones.count(),
    }
    return render(request, 'catalog.html', context)

# =============================================================================
# 🛒 BUYURTMA YARATISH (Xavfsiz va To'g'irlangan)
# =============================================================================

@require_POST
def create_order(request):
    try:
        # 1. Formdan kelgan ma'lumotlarni olish
        name = request.POST.get('name', '').strip()
        phone_num = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        payment_type = request.POST.get('payment_type', 'cash')
        items_json = request.POST.get('items', '[]')
        
        # HTML formadan 'loan_period' nomi bilan kelayotgan qiymatni olamiz
        raw_loan_period = request.POST.get('loan_period', '1')
        loan_period_val = int(raw_loan_period) if raw_loan_period.isdigit() else 1
        
        receipt_file = request.FILES.get('payment_receipt')

        # Majburiy maydonlar tekshiruvi
        if not name or not phone_num or not address:
            return HttpResponseBadRequest("Iltimos, barcha maydonlarni to'ldiring.")

        # 2. Savatni tahlil qilish va narxni qayta hisoblash
        try:
            cart_items = json.loads(items_json)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Savat ma'lumotlari noto'g'ri.")

        server_total = 0
        validated_items = []

        for item in cart_items:
            try:
                product = Phone.objects.get(id=item.get('id'))
                qty = int(item.get('qty', 1))
                
                # Narxni tekshirish (agar DB-da eski formatda bo'lsa)
                current_price = product.price
                if current_price > 100000000: # 100 mln dan baland bo'lsa
                    current_price = current_price // 100
                
                subtotal = current_price * qty
                server_total += subtotal
                
                validated_items.append({
                    'id': product.id,
                    'name': product.name,
                    'price': int(current_price),
                    'qty': qty,
                    'subtotal': int(subtotal)
                })
            except Phone.DoesNotExist:
                continue

        if not validated_items:
            return HttpResponseBadRequest("Savat bo'sh yoki mahsulotlar bazada yo'q.")

        # 3. Nasiya (Installment) foizini hisoblash
        final_total = server_total
        if payment_type == 'nasiya':
            markup_rates = {3: 0.05, 6: 0.10, 9: 0.15, 12: 0.20, 24: 0.35}
            markup = markup_rates.get(loan_period_val, 0.20)
            final_total = server_total * (1 + markup)

        # 4. BAZAGA SAQLASH (Modeldagi nomlar bilan moslashtirildi)
        order = Order.objects.create(
            customer_name=name,
            customer_phone=phone_num,
            address=address,
            items=json.dumps(validated_items, ensure_ascii=False),
            total_price=final_total,
            payment_method=payment_type,
            installment_period=loan_period_val, # loan_period -> installment_period bo'ldi
            payment_receipt=receipt_file
        )

        # 5. Telegramga bildirishnoma (Try-Except ichida, buyurtma to'xtab qolmasligi uchun)
        try:
            send_telegram_notification(order, validated_items, payment_type, final_total, receipt_file)
        except Exception as tg_err:
            logger.error(f"Telegram error: {tg_err}")

        # 6. Muvaffaqiyat sahifasiga o'tish
        request.session['order_id'] = order.id
        return redirect('phones:order_success')

    except Exception as e:
        logger.error(f"Buyurtma yaratishda xatolik: {e}", exc_info=True)
        return HttpResponseBadRequest(f"Xatolik yuz berdi: {str(e)}")

# =============================================================================
# 📩 TELEGRAM FUNKSIYASI
# =============================================================================

def send_telegram_notification(order, items, p_type, total, receipt=None):
    TOKEN = getattr(settings, 'TELEGRAM_BOT_TOKEN', os.getenv('TELEGRAM_BOT_TOKEN', ''))
    CHAT_ID = getattr(settings, 'TELEGRAM_CHAT_ID', os.getenv('TELEGRAM_CHAT_ID', ''))
    
    if not TOKEN or not CHAT_ID:
        return

    # Mahsulotlar ro'yxatini chiroyli qilish
    p_text = ""
    for i in items:
        price_f = f"{i['price']:,}".replace(',', ' ')
        p_text += f"• {i['name']} ({price_f} so'm) x {i['qty']}\n"

    p_method = "💰 Naqd" if p_type == 'cash' else f"💳 Nasiya ({order.installment_period} oy)"
    total_f = f"{int(total):,}".replace(',', ' ')

    message = (
        f"🚀 *YANGI BUYURTMA #{order.id}*\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 *Mijoz:* {order.customer_name}\n"
        f"📞 *Tel:* {order.customer_phone}\n"
        f"📍 *Manzil:* {order.address}\n\n"
        f"📦 *Mahsulotlar:*\n{p_text}\n"
        f"💳 *To'lov:* {p_method}\n"
        f"💰 *Jami:* {total_f} so'm"
    )

    try:
        if receipt:
            url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
            receipt.seek(0)
            files = {'photo': receipt}
            data = {'chat_id': CHAT_ID, 'caption': message, 'parse_mode': 'Markdown'}
            requests.post(url, files=files, data=data, timeout=10)
        else:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            data = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
            requests.post(url, data=data, timeout=10)
    except Exception as e:
        logger.error(f"Telegram API ulanish xatosi: {e}")

# =============================================================================
# ✅ QOLGAN FUNKSIYALAR
# =============================================================================

def order_success(request):
    order_id = request.session.pop('order_id', None)
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'success.html', {'order': order})
    return redirect('phones:home')

def product_suggestions(request):
    query = request.GET.get('q', '').strip()
    if len(query) >= 2:
        suggestions = Phone.objects.filter(name__icontains=query).values_list('name', flat=True)[:5]
        return JsonResponse(list(suggestions), safe=False)
    return JsonResponse([], safe=False)