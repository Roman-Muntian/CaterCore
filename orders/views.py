# orders/views.py
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.http import HttpResponse
from .forms import OrderCreateForm
from .models import Order, OrderItem
from cart.models import Cart
from services.payments import create_stripe_checkout_session, create_heleket_payment # Логіка з Task 3.6
from services.email import send_order_confirmation # Логіка з Task 3.6
import logging

logger = logging.getLogger(__name__)

def checkout_view(request):
    cart = request.cart
    if cart.total_items == 0:
        return redirect('catalog:index')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        payment_provider = request.POST.get('payment_provider') # 'stripe' or 'heleket'

        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = cart.total_price
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    dish=item.dish,
                    price=item.dish.price,
                    quantity=item.quantity
                )
            
            cart.items.all().delete() # Очищення кошика

            try:
                if payment_provider == 'stripe':
                    session = create_stripe_checkout_session(order, request)
                    # HTMX-First: редірект на стороні клієнта
                    response = HttpResponse(status=200)
                    response['HX-Redirect'] = session.url
                    return response
                
                elif payment_provider == 'heleket':
                    payment = create_heleket_payment(order, request)
                    response = HttpResponse(status=200)
                    response['HX-Redirect'] = payment['url']
                    return response

            except Exception as e:
                logger.error(f"Payment creation failed for order {order.id}: {e}")
                order.status = 'cancelled' # Або інший статус помилки
                order.save()
                # Повернути помилку для HTMX
                return TemplateResponse(request, 'orders/partials/checkout_error.html', {'error': str(e)})

    else:
        form = OrderCreateForm()
        if request.user.is_authenticated:
            form.initial.update({
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            })

    context = {'form': form, 'cart': cart}
    
    if request.htmx:
        # Можна реалізувати багатоетапну форму, повертаючи різні часткові шаблони
        return TemplateResponse(request, 'orders/partials/checkout_form.html', context)
        
    return TemplateResponse(request, 'orders/checkout.html', context)