# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Вказуємо поля, які будуть на формі реєстрації
        fields = ('first_name', 'last_name', 'email') 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Додаємо Tailwind класи до полів
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input w-full rounded border-gray-300'
            if field_name == 'email':
                 field.widget.attrs['placeholder'] = 'your.email@example.com'


class CustomUserChangeForm(UserChangeForm):
    # Видаляємо поле пароля з форми редагування профілю
    password = None 

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        # Поля, доступні для редагування в профілі
        fields = ('first_name', 'last_name', 'email', 'phone_number') 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input w-full rounded border-gray-300'


class CustomAuthenticationForm(AuthenticationForm):
    # Кастомізуємо форму входу, щоб використовувати email
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-input w-full rounded border-gray-300'})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-input w-full rounded border-gray-300'}),
    )