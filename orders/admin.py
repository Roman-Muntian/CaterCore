# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['dish']
    extra = 0
    readonly_fields = ('price',)

@admin.action(description="Змінити статус на 'Готується'")
def make_processing(modeladmin, request, queryset):
    queryset.update(status='processing')
    # Тут можна додати відправку email-сповіщення
    # for order in queryset:
    #     send_status_update(order)

@admin.action(description="Змінити статус на 'Виконано'")
def make_completed(modeladmin, request, queryset):
    queryset.update(status='completed')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'status', 'total_price', 'created_at', 'delivery_date', 'delivery_time')
    list_filter = ('status', 'delivery_date', 'created_at')
    search_fields = ('id', 'email', 'first_name', 'last_name', 'phone')
    readonly_fields = ('created_at', 'total_price', 'stripe_payment_intent_id', 'heleket_payment_id')
    inlines = [OrderItemInline]
    actions = [make_processing, make_completed]

    fieldsets = (
        ('Інформація про клієнта', {
            'fields': ('user', ('first_name', 'last_name'), ('email', 'phone'))
        }),
        ('Деталі доставки', {
            'fields': ('delivery_address', ('delivery_date', 'delivery_time'))
        }),
        ('Статус та Оплата', {
            'fields': ('status', 'total_price', 'stripe_payment_intent_id', 'heleket_payment_id')
        }),
    )
    
# orders/admin.py
# ... (існуючий код OrderItemInline, OrderAdmin) ...

# --- Реєстрація графіків ---
try:
    # Імпортуємо класи графіків з вашого файлу charts.py
    # Важливо: Шлях імпорту може бути 'CaterCore.charts', якщо 'CaterCore' - це назва вашого кореневого пакету проєкту
    from CaterCore.charts import OrdersPerDayChart, RevenuePerDayChart 

    admin.site.register(OrdersPerDayChart)
    admin.site.register(RevenuePerDayChart)
    print("Admin charts registered successfully.") # Додаємо для діагностики
except ImportError as e:
     print(f"Warning: Could not import or register admin charts: {e}") 
     # Можна додати більш детальне логування помилки імпорту
except Exception as e:
    print(f"An unexpected error occurred during chart registration: {e}")