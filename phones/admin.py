from django.contrib import admin
from .models import Phone, Order

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'is_installment_available')
    list_filter = ('brand', 'is_installment_available')
    search_fields = ('name', 'brand')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'total_price', 'created_at')
    readonly_fields = ('created_at',)