# services/payments.py
import stripe
import requests
import json
import base64
import hashlib
from django.conf import settings
from django.urls import reverse
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
HELEKET_API_KEY = settings.HELEKET_API_KEY
HELEKET_SECRET_KEY = settings.HELEKET_SECRET_KEY
HELEKET_BASE_URL = 'https://api.heleket.com/v1'

def create_stripe_checkout_session(order, request):
    line_items = [{
        'price_data': {
            'currency': 'pln', # Або інша валюта
            'product_data': {'name': item.dish.name},
            'unit_amount': int(item.price * 100),
        },
        'quantity': item.quantity,
    } for item in order.items.all()]

    session = stripe.checkout.Session.create(
        payment_method_types=['card', 'p24', 'blik'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('orders:order_success', args=[order.id])),
        cancel_url=request.build_absolute_uri(reverse('orders:order_cancel', args=[order.id])),
        metadata={'order_id': order.id}
    )
    order.stripe_payment_intent_id = session.payment_intent
    order.save()
    return session

def create_heleket_payment(order, request):
    payload = {
        'amount': f'{order.total_price:.2f}',
        'currency': 'USD', # Heleket може вимагати USD
        'order_id': str(order.id),
        'callback_url': request.build_absolute_uri(reverse('services:heleket_webhook')),
        'success_url': request.build_absolute_uri(reverse('orders:order_success', args=[order.id])),
        'fail_url': request.build_absolute_uri(reverse('orders:order_cancel', args=[order.id])),
    }
    
    # Логіка підпису Heleket (з enf/payment/views.py)
    payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=True)
    encoded_payload = base64.b64encode(payload_str.encode('utf-8')).decode('utf-8')
    sign = hashlib.md5((encoded_payload + HELEKET_SECRET_KEY).encode('utf-8')).hexdigest()

    headers = {
        'merchant': HELEKET_API_KEY,
        'sign': sign,
        'Content-Type': 'application/json',
    }
    
    response = requests.post(f"{HELEKET_BASE_URL}/payment", headers=headers, data=payload_str)
    response.raise_for_status()
    payment = response.json()
    
    if payment.get('state') == 0:
        order.heleket_payment_id = payment.get('result', {}).get('uuid')
        order.save()
        return payment['result']
    else:
        raise Exception(f'Heleket API error: {response.text}')