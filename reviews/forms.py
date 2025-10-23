# reviews/forms.py
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            # Додаємо класи Tailwind для стилізації
            'rating': forms.Select(attrs={'class': 'form-select w-full rounded border-gray-300'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea w-full rounded border-gray-300', 'placeholder': 'Ваш коментар...'}),
        }
        labels = {
            'rating': 'Оцінка',
            'comment': 'Коментар',
        }