# reviews/views.py
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Review
from catalog.models import Dish

@login_required
@require_POST
def add_review_view(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    form = ReviewForm(request.POST)
    
    if form.is_valid():
        # Створюємо або оновлюємо відгук
        review, created = Review.objects.update_or_create(
            dish=dish,
            user=request.user,
            defaults=form.cleaned_data
        )
        
        # Повертаємо оновлений список відгуків
        reviews = dish.reviews.all().order_by('-created_at')
        new_form = ReviewForm() # Чиста форма
        context = {'dish': dish, 'reviews': reviews, 'review_form': new_form}
        return TemplateResponse(request, 'reviews/partials/reviews_section.html', context)
    
    # Повертаємо форму з помилками
    reviews = dish.reviews.all().order_by('-created_at')
    context = {'dish': dish, 'reviews': reviews, 'review_form': form}
    return TemplateResponse(request, 'reviews/partials/reviews_section.html', context)