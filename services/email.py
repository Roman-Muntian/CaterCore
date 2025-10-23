# services/email.py
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_order_confirmation(order):
    subject = f'Ваше замовлення #{order.id} прийнято'
    html_message = render_to_string('services/email/order_confirmation.html', {'order': order})
    send_mail(
        subject,
        '', # plain text (можна згенерувати)
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        html_message=html_message
    )

def send_status_update(order):
    # Логіка для надсилання оновлень статусу
    pass