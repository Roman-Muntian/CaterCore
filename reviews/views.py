# reviews/views.py
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm # Потрібно створити цю форму
from .models import Review
from catalog.models import Dish

# Повертає partial ШАБЛОН СЕКЦІЇ ВІДГУКІВ (форма + список)
@require_GET # Цей ендпоінт тільки для GET-запитів
def review_list_view(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    reviews = dish.reviews.all().order_by('-created_at')
    
    # Якщо користувач залогінений, показуємо йому форму
    # (можливо, з його попереднім відгуком)
    initial_data = {}
    if request.user.is_authenticated:
        user_review = Review.objects.filter(dish=dish, user=request.user).first()
        if user_review:
            initial_data = {'rating': user_review.rating, 'comment': user_review.comment}
            
    review_form = ReviewForm(initial=initial_data)

    context = {
        'dish': dish,
        'reviews': reviews,
        'review_form': review_form
    }
    # Завжди повертаємо partial, бо цей view викликається тільки через HTMX
    return TemplateResponse(request, 'reviews/partials/review_section.html', context)


@login_required # Тільки залогінені можуть додавати відгуки
@require_POST # Цей ендпоінт тільки для POST-запитів
def add_review_view(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    form = ReviewForm(request.POST)
    
    if form.is_valid():
        # Використовуємо update_or_create, щоб користувач міг змінити свій відгук
        review, created = Review.objects.update_or_create(
            dish=dish,
            user=request.user,
            defaults=form.cleaned_data # Оновлюємо або створюємо з даними форми
        )
        
        # --- HTMX Response (Успіх) ---
        # Повертаємо оновлену секцію відгуків (з новим відгуком та чистою формою)
        reviews = dish.reviews.all().order_by('-created_at')
        new_form = ReviewForm() # Чиста форма для наступного разу
        context = {'dish': dish, 'reviews': reviews, 'review_form': new_form}
        return TemplateResponse(request, 'reviews/partials/review_section.html', context)
    
    else:
        # --- HTMX Response (Помилка валідації) ---
        # Повертаємо секцію відгуків з тією ж формою, але тепер з помилками
        reviews = dish.reviews.all().order_by('-created_at')
        context = {'dish': dish, 'reviews': reviews, 'review_form': form} # Передаємо форму з помилками
        return TemplateResponse(request, 'reviews/partials/review_section.html', context)