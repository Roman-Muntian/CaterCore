# services/email.py
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _ # Для перекладу тем листів

logger = logging.getLogger(__name__)

def send_order_confirmation(order):
    """Надсилає лист-підтвердження після успішної оплати/створення замовлення."""
    subject = _("Ваше замовлення #{order_id} прийнято!").format(order_id=order.id)
    
    # Використовуємо HTML-шаблон для листа
    try:
        html_message = render_to_string('services/email/order_confirmation.html', {'order': order})
        # Створюємо простий текстовий варіант (опціонально, але рекомендовано)
        plain_message = render_to_string('services/email/order_confirmation.txt', {'order': order})
        
        send_mail(
            subject=subject,
            message=plain_message, # Текстовий варіант
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            html_message=html_message, # HTML-варіант
            fail_silently=False, # Щоб бачити помилки надсилання
        )
        logger.info(f"Order confirmation email sent successfully for order {order.id} to {order.email}.")
    except Exception as e:
        logger.error(f"Failed to send order confirmation email for order {order.id}: {e}")

def send_status_update(order):
    """Надсилає лист при зміні статусу замовлення (напр., "Готується", "В дорозі")."""
    subject_map = {
        'processing': _("Ваше замовлення #{order_id} готується!").format(order_id=order.id),
        'shipping': _("Ваше замовлення #{order_id} в дорозі!").format(order_id=order.id),
        'completed': _("Ваше замовлення #{order_id} виконано!").format(order_id=order.id),
        'cancelled': _("Ваше замовлення #{order_id} скасовано.").format(order_id=order.id),
    }
    subject = subject_map.get(order.status)
    
    if not subject:
        logger.warning(f"No email template defined for order status '{order.status}' (Order {order.id}).")
        return

    try:
        # Можна створити різні шаблони для різних статусів
        template_name = f'services/email/status_{order.status}.html' 
        html_message = render_to_string(template_name, {'order': order})
        plain_message = render_to_string(f'services/email/status_{order.status}.txt', {'order': order})
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Order status update email ('{order.status}') sent for order {order.id} to {order.email}.")
    except Exception as e:
        logger.error(f"Failed to send status update email for order {order.id} (status: {order.status}): {e}")