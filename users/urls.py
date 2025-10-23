# users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Автентифікація (використовуємо кастомні views)
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'), # Наш view з HTMX логікою

    # Особистий кабінет
    path('profile/', views.profile_view, name='profile'),
    
    # --- HTMX Endpoints для профілю ---
    # GET: Повертає форму редагування
    path('profile/edit/', views.profile_edit_view, name='profile_edit'), 
    # POST: Оновлює дані (з форми profile_edit)
    # GET (альтернативно): Повертає partial з деталями профілю (для кнопки "Скасувати")
    path('profile/details/', views.profile_details_view, name='profile_details'), 
    # GET: Повертає partial з історією замовлень
    path('profile/orders/', views.order_history_view, name='order_history'), 
]