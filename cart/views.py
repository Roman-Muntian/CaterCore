# cart/views.py
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.template.response import TemplateResponse
from django.http import HttpResponse
from .models import CartItem
from catalog.models import Dish
from django.db.models import F

# Повертає ШАБЛОН МОДАЛЬНОГО ВІКНА (оболонку з Alpine.js)
def cart_detail_view(request):
    # Цей view викликається при кліку на іконку кошика
    # Він повертає HTML оболонки, яка потім через hx-get="cart:cart_content"
    # сама завантажить свій вміст.
    return TemplateResponse(request, 'cart/partials/cart_modal.html')

# Повертає ВМІСТ МОДАЛЬНОГО ВІКНА (список товарів, кнопки)
def cart_content_view(request):
    # Цей view викликається з cart_modal.html через hx-get,
    # а також після додавання/видалення товару.
    context = {'cart': request.cart}
    return TemplateResponse(request, 'cart/partials/cart_modal_content.html', context)

# Повертає ОНОВЛЕНУ ІКОНКУ ХЕДЕРА
def cart_icon_view(request):
    # Цей view викликається з cart_icon.html через hx-get по тригеру.
    context = {'cart_total_items': request.cart.total_items}
    return TemplateResponse(request, 'partials/cart_icon.html', context)

@require_POST
def cart_add_view(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    
    # Використовуємо get_or_create для додавання або збільшення кількості
    item, created = CartItem.objects.get_or_create(
        cart=request.cart, 
        dish=dish,
        defaults={'quantity': 1}
    )
    
    if not created:
        item.quantity = F('quantity') + 1
        item.save()

    # --- HTMX Response ---
    # Повертаємо оновлений ВМІСТ кошика
    context = {'cart': request.cart}
    response = TemplateResponse(request, 'cart/partials/cart_modal_content.html', context)
    # І ТАКОЖ відправляємо подію для оновлення іконки в хедері
    response['HX-Trigger'] = 'update-cart-icon' 
    return response

@require_POST
def cart_remove_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart=request.cart)
    item.delete()
    
    # --- HTMX Response ---
    # Повертаємо оновлений ВМІСТ кошика
    context = {'cart': request.cart}
    response = TemplateResponse(request, 'cart/partials/cart_modal_content.html', context)
    # І ТАКОЖ відправляємо подію для оновлення іконки в хедері
    response['HX-Trigger'] = 'update-cart-icon'
    return response

# --- Додатково: Оновлення кількості (приклад) ---
# @require_POST
# def cart_update_view(request, item_id):
#     item = get_object_or_404(CartItem, id=item_id, cart=request.cart)
#     new_quantity = int(request.POST.get('quantity', 1))
    
#     if new_quantity > 0:
#         item.quantity = new_quantity
#         item.save()
#     else:
#         item.delete() # Видаляємо, якщо кількість 0 або менше
        
#     context = {'cart': request.cart}
#     response = TemplateResponse(request, 'cart/partials/cart_modal_content.html', context)
#     response['HX-Trigger'] = 'update-cart-icon'
#     return response