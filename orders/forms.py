# orders/forms.py
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'delivery_address', 'delivery_date', 'delivery_time'
        ]