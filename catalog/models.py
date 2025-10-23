# catalog/models.py
from django.db import models
from django.db.models import Avg
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Dish(models.Model):
    category = models.ForeignKey(Category, related_name='dishes', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight_grams = models.PositiveIntegerField(help_text="Вага в грамах")
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:dish_detail', args=[self.slug])
        
    @property
    def average_rating(self):
        # Розрахунок середнього рейтингу з reviews.Review
        return self.reviews.aggregate(Avg('rating'))['rating__avg']