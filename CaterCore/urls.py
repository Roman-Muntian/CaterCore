# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # # Вебхуки та API поза i18n
    # path('services/', include('services.urls', namespace='services')),
]

# Маршрути, що підтримують переклад
urlpatterns += i18n_patterns(
    # path('users/', include('users.urls', namespace='users')),
    # path('cart/', include('cart.urls', namespace='cart')),
    # path('orders/', include('orders.urls', namespace='orders')),
    # path('reviews/', include('reviews.urls', namespace='reviews')),
    # path('', include('catalog.urls', namespace='catalog')),
    
    # Flatpages (має бути останнім)
    # path('', include('django.contrib.flatpages.urls')),
)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]