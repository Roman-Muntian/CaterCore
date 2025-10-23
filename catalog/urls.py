# catalog/urls.py
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Головна сторінка каталогу (всі страви)
    path('', views.dish_list_view, name='index'), 
    
    # Сторінка категорії
    path('category/<slug:category_slug>/', views.dish_list_view, name='category_detail'),
    
    # Сторінка деталей страви
    path('dish/<slug:slug>/', views.dish_detail_view, name='dish_detail'),
]