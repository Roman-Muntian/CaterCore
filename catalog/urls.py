# catalog/urls.py
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Це URL, який ми використовуємо в base.html
    path('', views.dish_list_view, name='index'), 
    
    # Ми додамо їх пізніше, але вони потрібні для посилань
    path('dish/<slug:slug>/', views.dish_detail_view, name='dish_detail'),
    path('category/<slug:category_slug>/', views.dish_list_view, name='category_detail'),
]