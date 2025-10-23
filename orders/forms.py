# orders/forms.py
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        # Включаємо поля, які користувач заповнює при оформленні
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'delivery_address', 'delivery_date', 'delivery_time'
        ]
        widgets = {
            # Додаємо класи Tailwind та типи для зручності
            'first_name': forms.TextInput(attrs={'class': 'form-input w-full rounded border-gray-300'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input w-full rounded border-gray-300'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-full rounded border-gray-300'}),
            'phone': forms.TextInput(attrs={'class': 'form-input w-full rounded border-gray-300'}),
            'delivery_address': forms.TextInput(attrs={'id': 'id_delivery_address', 'class': 'form-input w-full rounded border-gray-300'}), # ID для Google Maps
            'delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input w-full rounded border-gray-300'}),
            'delivery_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input w-full rounded border-gray-300'}),
        }
        labels = {
            'first_name': "Ім'я",
            'last_name': 'Прізвище',
            'email': 'Email',
            'phone': 'Телефон',
            'delivery_address': 'Адреса доставки',
            'delivery_date': 'Дата доставки',
            'delivery_time': 'Час доставки',
        }