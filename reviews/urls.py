# reviews/urls.py
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # GET-запит для завантаження секції відгуків (викликається з dish_detail.html)
    path('list/<int:dish_id>/', views.review_list_view, name='review_list'),
    
    # POST-запит для додавання/оновлення відгуку (викликається з форми)
    path('add/<int:dish_id>/', views.add_review_view, name='add_review'),
]