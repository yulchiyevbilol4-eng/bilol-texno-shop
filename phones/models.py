from django.db import models

class Phone(models.Model):
    name = models.CharField(max_length=200, verbose_name="Telefon nomi")
    brand = models.CharField(max_length=100, verbose_name="Brend", blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Narxi (so'm)")
    image = models.ImageField(upload_to='phones/', verbose_name="Rasm")
    description = models.TextField(verbose_name="Tavsif", blank=True, null=True)
    
    ram = models.IntegerField(default=8, verbose_name="RAM (GB)")
    memory = models.IntegerField(default=128, verbose_name="Xotira (GB)")
    battery = models.IntegerField(default=5000, verbose_name="Batareya (mAh)")
    is_installment_available = models.BooleanField(default=True, verbose_name="Nasiya mavjud")

    def __str__(self):
        return f"{self.name} - {self.price} so'm"

    class Meta:
        verbose_name = "Telefon"
        verbose_name_plural = "Telefonlar"

class Order(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name="Mijoz ismi")
    customer_phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    address = models.TextField(verbose_name="Manzil", default="Do'kondan olib ketish")
    items = models.TextField(verbose_name="Mahsulotlar (JSON)")
    payment_method = models.CharField(max_length=50, verbose_name="To'lov turi")
    
    # Nasiya ma'lumotlari - views.py bilan mos kelishi kerak
    installment_period = models.IntegerField(null=True, blank=True, verbose_name="Muddat (oy)")
    monthly_payment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Oylik to'lov")
    
    payment_receipt = models.ImageField(upload_to='receipts/', null=True, blank=True, verbose_name="To'lov cheki")
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Umumiy summa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"