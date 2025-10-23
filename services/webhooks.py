# services/webhooks.py
import stripe
import json
import hashlib
import base64
import logging
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from orders.models import Order
from .email import send_order_confirmation, send_status_update # Імпортуємо функцію надсилання листів

logger = logging.getLogger(__name__)

@csrf_exempt # Вимикаємо CSRF-перевірку для зовнішніх запитів
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Неправильний payload
        logger.error(f"Stripe Webhook ValueError: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Неправильний підпис
        logger.error(f"Stripe Webhook SignatureVerificationError: {e}")
        return HttpResponse(status=400)
    except Exception as e:
        logger.error(f"Stripe Webhook unexpected error: {e}")
        return HttpResponse(status=500)

    # Обробка події checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')
        payment_intent_id = session.get('payment_intent')
        
        logger.info(f"Stripe checkout.session.completed received for order_id: {order_id}")

        if order_id:
            try:
                order = get_object_or_404(Order, id=order_id)
                
                # Перевіряємо, чи замовлення ще не оброблено
                if order.status == 'pending':
                    order.status = 'processing' # Статус "Готується"
                    order.stripe_payment_intent_id = payment_intent_id # Зберігаємо ID платежу
                    order.save()
                    
                    logger.info(f"Order {order_id} status updated to 'processing' via Stripe webhook.")
                    
                    # Надсилаємо email-підтвердження
                    send_order_confirmation(order)
                    
                else:
                    logger.warning(f"Order {order_id} already processed (current status: {order.status}). Ignoring Stripe webhook.")
                    
            except Order.DoesNotExist:
                logger.error(f"Order {order_id} not found for Stripe webhook.")
                return HttpResponse(status=404)
            except Exception as e:
                 logger.error(f"Error processing Stripe webhook for order {order_id}: {e}")
                 return HttpResponse(status=500)
        else:
            logger.warning("Stripe webhook received without order_id in metadata.")

    # Можна додати обробку інших подій Stripe, наприклад, 'payment_intent.payment_failed'

    return HttpResponse(status=200)


@csrf_exempt
def heleket_webhook(request):
    signature = request.headers.get('sign')
    payload = request.body.decode('utf-8')

    # Перевірка підпису Heleket (з enf)
    try:
        encoded_payload = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
        expected_signature = hashlib.md5((encoded_payload + settings.HELEKET_SECRET_KEY).encode('utf-8')).hexdigest()

        if not signature or signature != expected_signature:
            logger.warning("Heleket Webhook: Invalid signature.")
            return HttpResponseBadRequest('Invalid signature')
            
        data = json.loads(payload)
    except (json.JSONDecodeError, Exception) as e:
         logger.error(f"Heleket Webhook payload/signature error: {e}")
         return HttpResponseBadRequest('Invalid payload or signature calculation error')

    # Обробка даних Heleket
    result = data.get('result', {})
    order_id = result.get('order_id')
    payment_status = result.get('payment_status') # 'paid', 'fail', 'cancel', etc.
    payment_uuid = result.get('uuid')

    logger.info(f"Heleket webhook received for order_id: {order_id}, status: {payment_status}")

    if order_id:
        try:
            order = get_object_or_404(Order, id=order_id)
            
            # Обробка успішної оплати
            if payment_status == 'paid' and order.status == 'pending':
                order.status = 'processing' # Статус "Готується"
                order.heleket_payment_id = payment_uuid # Зберігаємо ID платежу
                order.save()
                
                logger.info(f"Order {order_id} status updated to 'processing' via Heleket webhook.")
                
                # Надсилаємо email-підтвердження
                send_order_confirmation(order)
                
            # Обробка неуспішної оплати
            elif payment_status in ['fail', 'cancel', 'system_fail', 'wrong_amount'] and order.status == 'pending':
                order.status = 'cancelled'
                order.save()
                logger.info(f"Order {order_id} status updated to 'cancelled' via Heleket webhook (status: {payment_status}).")
                # Тут можна надіслати лист про скасування
                
            # Ігноруємо, якщо статус вже змінено
            elif order.status != 'pending':
                 logger.warning(f"Order {order_id} already processed (current status: {order.status}). Ignoring Heleket webhook.")

        except Order.DoesNotExist:
            logger.error(f"Order {order_id} not found for Heleket webhook.")
            return HttpResponse(status=404)
        except Exception as e:
            logger.error(f"Error processing Heleket webhook for order {order_id}: {e}")
            return HttpResponse(status=500)
    else:
        logger.warning("Heleket webhook received without order_id.")

    return HttpResponse(status=200)