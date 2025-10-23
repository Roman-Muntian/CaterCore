# services/urls.py
from django.urls import path
from . import webhooks # Створимо цей файл

app_name = 'services'

urlpatterns = [
    # Ендпоінти для отримання сповіщень від платіжних систем
    path('webhooks/stripe/', webhooks.stripe_webhook, name='stripe_webhook'),
    path('webhooks/heleket/', webhooks.heleket_webhook, name='heleket_webhook'),
]