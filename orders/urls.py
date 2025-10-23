# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Сторінка оформлення замовлення (GET + POST/HTMX)
    path('checkout/', views.checkout_view, name='checkout'),
    
    # Сторінки статусу (куди редіректить Stripe/Heleket)
    path('success/<int:order_id>/', views.order_success_view, name='order_success'),
    path('cancel/<int:order_id>/', views.order_cancel_view, name='order_cancel'),
]