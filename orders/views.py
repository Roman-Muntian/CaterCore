# orders/views.py (доповнення)
from django.shortcuts import render, redirect, get_object_or_404 # Додаємо get_object_or_404
from django.template.response import TemplateResponse
from django.http import HttpResponse
from .forms import OrderCreateForm
from .models import Order, OrderItem
from cart.models import Cart
from services.payments import create_stripe_checkout_session, create_heleket_payment 
from services.email import send_order_confirmation
import logging

logger = logging.getLogger(__name__)

# --- checkout_view (з невеликими змінами для URL) ---
def checkout_view(request):
    cart = request.cart
    if cart.total_items == 0:
        return redirect('catalog:index')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        payment_provider = request.POST.get('payment_provider') 

        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = cart.total_price
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order, dish=item.dish, price=item.dish.price, quantity=item.quantity
                )
            
            # Очищаємо кошик ТІЛЬКИ ПІСЛЯ успішного створення платежу
            # cart.items.all().delete() # <--- Перенесемо це

            try:
                redirect_url = None
                if payment_provider == 'stripe':
                    session = create_stripe_checkout_session(order, request) # Тепер передаємо order_id в success/cancel URL
                    redirect_url = session.url
                elif payment_provider == 'heleket':
                    payment = create_heleket_payment(order, request) # Тепер передаємо order_id в success/cancel URL
                    redirect_url = payment['url']
                
                if redirect_url:
                    cart.items.all().delete() # Очищаємо кошик тут
                    # --- HTMX Logic ---
                    if request.htmx:
                        response = HttpResponse(status=200)
                        response['HX-Redirect'] = redirect_url
                        return response
                    else: # Звичайний POST
                         return redirect(redirect_url)
                else:
                     raise Exception("Payment provider not specified or invalid.")

            except Exception as e:
                logger.error(f"Payment creation failed for order {order.id}: {e}")
                order.status = 'cancelled' # Або інший статус помилки
                order.save()
                # --- HTMX Logic (Помилка) ---
                context = {'form': form, 'cart': cart, 'error_message': str(e)}
                return TemplateResponse(request, 'orders/partials/checkout_form.html', context, status=400) # Повертаємо 400 статус

        else: # Форма не валідна
            # --- HTMX Logic (Помилка валідації) ---
            context = {'form': form, 'cart': cart}
            return TemplateResponse(request, 'orders/partials/checkout_form.html', context, status=400) 

    else: # GET запит
        form = OrderCreateForm()
        if request.user.is_authenticated:
            form.initial.update({
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'phone': request.user.phone_number, # Додали телефон
            })

    context = {'form': form, 'cart': cart}
    
    # --- HTMX Logic (GET) ---
    if request.htmx:
        return TemplateResponse(request, 'orders/partials/checkout_form.html', context)
        
    return TemplateResponse(request, 'orders/checkout.html', context)

# --- Нові Views для Success/Cancel ---

def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Перевіряємо, чи це замовлення поточного користувача (якщо він залогінений)
    if order.user and order.user != request.user:
         return redirect('catalog:index') # Або показати помилку
         
    # Тут можна додати логіку перевірки статусу оплати, якщо вебхук ще не спрацював
    # send_order_confirmation(order) # Можливо, краще надсилати лист після вебхука
    
    context = {'order': order}
    # --- HTMX Logic ---
    if request.htmx:
         # Якщо користувач прийшов сюди через HTMX-редірект
         return TemplateResponse(request, 'orders/partials/order_success_content.html', context)
         
    return render(request, 'orders/order_success.html', context)


def order_cancel_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user and order.user != request.user:
         return redirect('catalog:index')
         
    # Зазвичай, платіжна система вже встановила б статус 'cancelled' через вебхук,
    # але ми можемо встановити його тут про всяк випадок.
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        
    context = {'order': order}
    # --- HTMX Logic ---
    if request.htmx:
        return TemplateResponse(request, 'orders/partials/order_cancel_content.html', context)
        
    return render(request, 'orders/order_cancel.html', context)