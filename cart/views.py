# cart/views.py
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.template.response import TemplateResponse
from django.http import HttpResponse
from .models import Cart, CartItem
from catalog.models import Dish
from django.db.models import F

def cart_detail_view(request):
    context = {'cart': request.cart}
    # Головний HTMX-endpoint для модального вікна кошика
    return TemplateResponse(request, 'cart/partials/cart_modal.html', context)

@require_POST
def cart_add_view(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    
    item, created = CartItem.objects.get_or_create(
        cart=request.cart, 
        dish=dish,
        defaults={'quantity': 1}
    )
    
    if not created:
        item.quantity = F('quantity') + 1
        item.save()

    # Повертаємо два часткових шаблони: один для кошика, інший для іконки
    context = {'cart': request.cart}
    response = TemplateResponse(request, 'cart/partials/cart_modal_content.html', context)
    response['HX-Trigger'] = 'update-cart-icon' # Тригер для оновлення іконки
    return response

@require_POST
def cart_remove_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart=request.cart)
    item.delete()
    
    context = {'cart': request.cart}
    response = TemplateResponse(request, 'cart/partials/cart_modal_content.html', context)
    response['HX-Trigger'] = 'update-cart-icon'
    return response

# Endpoint для оновлення іконки кошика в хедері
def cart_icon_view(request):
    context = {'total_items': request.cart.total_items}
    return TemplateResponse(request, 'cart/partials/cart_icon.html', context)