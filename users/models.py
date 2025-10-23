# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# --- 1. ДОДАЙТЕ ЦЕЙ КЛАС МЕНЕДЖЕРА ---
class CustomUserManager(BaseUserManager):
    """
    Кастомний менеджер користувачів, де email є унікальним
    ідентифікатором замість username.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Створює та зберігає користувача з email та паролем.
        """
        if not email:
            raise ValueError(_('Email (електронна пошта) є обов\'язковим полем'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Створює та зберігає суперкористувача з email та паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        # 'first_name' та 'last_name' будуть автоматично запитані 
        # командою createsuperuser, оскільки вони в REQUIRED_FIELDS
        
        return self.create_user(email, password, **extra_fields)
# ----------------------------------------


class CustomUser(AbstractUser):
    # Видаляємо username
    username = None 
    
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # --- 2. ДОДАЙТЕ ЦЕЙ РЯДОК ---
    objects = CustomUserManager() # Вказуємо Django використовувати наш менеджер
    # ----------------------------

    def __str__(self):
        return self.email