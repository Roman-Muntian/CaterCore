# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.views.decorators.http import require_POST # <--- ОСЬ ЦЕЙ ІМПОРТ

from .models import CustomUser
from orders.models import Order 
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm

# --- Автентифікація ---

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:index') 

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

# Використовуємо require_POST та перевірку htmx для безпечного виходу
@require_POST # <--- Тепер цей декоратор відомий
def logout_view(request):
    logout(request)
    if request.htmx:
        response = HttpResponse()
        response['HX-Redirect'] = reverse('catalog:index')
        return response
    return redirect('catalog:index')

# --- Особистий кабінет ---
# ... (решта коду залишається без змін) ...

@login_required 
def profile_view(request):
    context = {'user': request.user}
    return TemplateResponse(request, 'users/profile.html', context)

@login_required
def profile_details_view(request):
    context = {'user': request.user}
    return TemplateResponse(request, 'users/partials/profile_details.html', context)

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            context = {'user': request.user}
            return TemplateResponse(request, 'users/partials/profile_details.html', context)
        else:
            context = {'form': form}
            return TemplateResponse(request, 'users/partials/profile_form.html', context)
    else: 
        form = CustomUserChangeForm(instance=request.user)
        context = {'form': form}
        return TemplateResponse(request, 'users/partials/profile_form.html', context)

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {'orders': orders}
    return TemplateResponse(request, 'users/partials/order_history.html', context)