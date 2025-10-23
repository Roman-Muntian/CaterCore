# cart/urls.py
from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    # Потрібно для base.html
    path('icon/', views.cart_icon_view, name='cart_icon'),
]