# catalog/views.py
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from .models import Dish, Category
from reviews.forms import ReviewForm # Потрібно створити цю форму

def dish_list_view(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    dishes = Dish.objects.filter(is_available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        dishes = dishes.filter(category=category)
        
    context = {
        'category': category,
        'categories': categories,
        'dishes': dishes
    }
    
    # --- HTMX Logic ---
    if request.htmx:
        # Для HTMX-запитів повертаємо ЛИШЕ список страв
        return TemplateResponse(request, 'catalog/partials/dish_list.html', context)
        
    # Для звичайних запитів повертаємо повний шаблон
    return TemplateResponse(request, 'catalog/dish_list.html', context)

def dish_detail_view(request, slug):
    dish = get_object_or_404(Dish, slug=slug, is_available=True)
    # Відгуки будуть завантажені окремим HTMX-запитом до `reviews`
    
    context = {
        'dish': dish,
        # 'review_form': ReviewForm() # Додамо, коли створимо форму
    }
    
    # --- HTMX Logic ---
    if request.htmx:
        # Повертаємо ЛИШЕ вміст сторінки (без base.html)
        return TemplateResponse(request, 'catalog/partials/dish_detail_content.html', context)

    # Для звичайних запитів повертаємо повний шаблон
    return TemplateResponse(request, 'catalog/dish_detail.html', context)