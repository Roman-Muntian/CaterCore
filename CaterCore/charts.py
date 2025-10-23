# config/charts.py
from admin_charts.admin import AdminChart
from orders.models import Order
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay

class OrdersPerDayChart(AdminChart):
    chart_type = 'line'
    title = 'Замовлення по днях'
    
    def get_data(self):
        queryset = (
            Order.objects
            .annotate(day=TruncDay('created_at'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        return queryset.values_list('day', 'count')

class RevenuePerDayChart(AdminChart):
    chart_type = 'bar'
    title = 'Дохід по днях (Виконані замовлення)'
    
    def get_data(self):
        queryset = (
            Order.objects.filter(status='completed')
            .annotate(day=TruncDay('created_at'))
            .values('day')
            .annotate(total=Sum('total_price'))
            .order_by('day')
        )
        return queryset.values_list('day', 'total')

# Потрібно зареєструвати в config/admin.py (або в orders/admin.py)
# from django.contrib import admin
# from .charts import OrdersPerDayChart, RevenuePerDayChart
# admin.site.register(OrdersPerDayChart)
# admin.site.register(RevenuePerDayChart)