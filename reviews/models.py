# reviews/models.py
from django.db import models
from django.conf import settings
from catalog.models import Dish
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    dish = models.ForeignKey(Dish, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('dish', 'user') # Користувач може лишити 1 відгук на 1 страву