# orders/models.py
from django.db import models
from django.conf import settings
from catalog.models import Dish

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Прийнято'),
        ('processing', 'Готується'),
        ('shipping', 'В дорозі'),
        ('completed', 'Виконано'),
        ('cancelled', 'Скасовано'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='orders')
    # Поля для анонімних
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    
    delivery_address = models.CharField(max_length=255)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Поля для платежів
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    heleket_payment_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Ціна на момент покупки
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.dish.name} ({self.quantity})"