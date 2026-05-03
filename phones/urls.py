from django.urls import path
from . import views

app_name = 'phones'  # Namespace - URL'larni nomlash uchun muhim

urlpatterns = [
    # ✅ Bosh sahifa
    path('', views.home, name='home'),
    
    # ✅ Mahsulot batafsil sahifasi
    path('phone/<int:pk>/', views.phone_detail, name='phone_detail'),
    
    # ✅ Buyurtma yaratish (POST so'rovlar uchun)
    path('create-order/', views.create_order, name='create_order'),
    
    # ✅ Buyurtma muvaffaqiyatli sahifasi (GET so'rovlar uchun)
    path('order-success/', views.order_success, name='order_success'),
    
    # ✅ Qidiruv takliflari (AJAX)
    path('suggestions/', views.product_suggestions, name='product_suggestions'),
    
    # ✅ Qo'shimcha sahifalar
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('catalog/', views.catalog, name='catalog'),
]