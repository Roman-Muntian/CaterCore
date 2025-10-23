# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.template.response import TemplateResponse
from django.http import HttpResponse

from .models import CustomUser
from orders.models import Order 
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm

# --- Автентифікація ---

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm # Використовуємо нашу форму

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:index') # Редірект після успішної реєстрації

    def form_valid(self, form):
        # Автоматично логінимо користувача після реєстрації
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

# Використовуємо require_POST та перевірку htmx для безпечного виходу
@require_POST 
def logout_view(request):
    logout(request)
    # --- HTMX Logic ---
    if request.htmx:
        # Відправляємо заголовок HX-Redirect, HTMX зробить редірект на клієнті
        response = HttpResponse()
        response['HX-Redirect'] = reverse('catalog:index')
        return response
    # Звичайний редірект для не-HTMX запитів
    return redirect('catalog:index')

# --- Особистий кабінет ---

@login_required # Доступ тільки для залогінених
def profile_view(request):
    # Цей view повертає ПОВНИЙ шаблон профілю.
    # Історія замовлень та форма редагування завантажуються окремими HTMX-запитами.
    context = {
        'user': request.user, 
    }
    return TemplateResponse(request, 'users/profile.html', context)

@login_required
def profile_details_view(request):
    # --- HTMX Endpoint (GET) ---
    # Повертає PARTIAL з деталями профілю.
    # Використовується для початкового завантаження та кнопки "Скасувати".
    context = {'user': request.user}
    return TemplateResponse(request, 'users/partials/profile_details.html', context)

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # --- HTMX Response (Успіх POST) ---
            # Повертаємо оновлений partial з деталями профілю
            context = {'user': request.user}
            return TemplateResponse(request, 'users/partials/profile_details.html', context)
        else:
            # --- HTMX Response (Помилка POST) ---
            # Повертаємо partial з формою та помилками валідації
            context = {'form': form}
            return TemplateResponse(request, 'users/partials/profile_form.html', context)
    else: # GET запит
        form = CustomUserChangeForm(instance=request.user)
        # --- HTMX Response (GET) ---
        # Повертаємо partial з формою редагування
        context = {'form': form}
        return TemplateResponse(request, 'users/partials/profile_form.html', context)


@login_required
def order_history_view(request):
    # --- HTMX Endpoint (GET) ---
    # Повертає PARTIAL з історією замовлень.
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {'orders': orders}
    return TemplateResponse(request, 'users/partials/order_history.html', context)