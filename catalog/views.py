# catalog/views.py
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from .models import Dish, Category
from reviews.forms import ReviewForm # Імпортуємо форму відгуків

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
    
    # HTMX-First: перевірка заголовка
    if request.htmx:
        return TemplateResponse(request, 'catalog/partials/dish_list.html', context)
        
    return TemplateResponse(request, 'catalog/dish_list.html', context)

def dish_detail_view(request, slug):
    dish = get_object_or_404(Dish, slug=slug, is_available=True)
    reviews = dish.reviews.all().order_by('-created_at')
    review_form = ReviewForm() # Форма для нового відгуку

    context = {
        'dish': dish,
        'reviews': reviews,
        'review_form': review_form
    }
    
    if request.htmx:
        return TemplateResponse(request, 'catalog/partials/dish_detail.html', context)

    return TemplateResponse(request, 'catalog/dish_detail.html', context)