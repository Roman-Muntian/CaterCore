# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.template.response import TemplateResponse
from django.http import HttpResponse

from .models import CustomUser
from orders.models import Order
# Потрібно створити ці форми
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

def logout_view(request):
    logout(request)
    if request.htmx:
        response = HttpResponse()
        response['HX-Redirect'] = reverse_lazy('catalog:index')
        return response
    return redirect('catalog:index')

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'user': request.user,
        'orders': orders
    }
    return TemplateResponse(request, 'users/profile.html', context)

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    context = {'form': form}
    
    # HTMX-First: повертаємо частковий шаблон
    if request.htmx:
        return TemplateResponse(request, 'users/partials/profile_form.html', context)
        
    return TemplateResponse(request, 'users/profile_edit.html', context)