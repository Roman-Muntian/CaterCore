# cart/urls.py
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # --- HTMX Endpoints ---
    # Повертає "оболонку" модального вікна (з Alpine.js)
    path('modal/', views.cart_detail_view, name='cart_detail'), 
    # Повертає вміст модального вікна (список товарів)
    path('content/', views.cart_content_view, name='cart_content'), 
    # Повертає оновлену іконку хедера
    path('icon/', views.cart_icon_view, name='cart_icon'), 
    
    # Дії
    path('add/<int:dish_id>/', views.cart_add_view, name='cart_add'),
    path('remove/<int:item_id>/', views.cart_remove_view, name='cart_remove'),
    # Додатково: Оновлення кількості (якщо потрібно)
    # path('update/<int:item_id>/', views.cart_update_view, name='cart_update'), 
]