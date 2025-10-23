# services/webhooks.py
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import stripe
import json
import hashlib
import base64
from django.conf import settings
from orders.models import Order
from .email import send_order_confirmation

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')
        if order_id:
            order = get_object_or_404(Order, id=order_id)
            order.status = 'processing' # "Готується"
            order.save()
            send_order_confirmation(order) # Надсилаємо лист
            
    return HttpResponse(status=200)

@csrf_exempt
def heleket_webhook(request):
    # Логіка валідації підпису Heleket (з enf)
    # ... (пропущено для стислості) ...
    
    data = json.loads(request.body)
    order_id = data.get('result', {}).get('order_id')
    status = data.get('result', {}).get('payment_status')

    if order_id:
        order = get_object_or_404(Order, id=order_id)
        if status == 'paid' and order.status == 'pending':
            order.status = 'processing' # "Готується"
            order.save()
            send_order_confirmation(order) # Надсилаємо лист
        elif status in ['fail', 'cancel']:
             order.status = 'cancelled'
             order.save()
             
    return HttpResponse(status=200)