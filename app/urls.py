from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from .views import MainSearch
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('api/', include('supplier.urls')),
    path('api/', include('customer.urls')),
    path('api/', include('order.urls')),
    path('api/', include('sale.urls')),
    path('api/', include('store.urls')),
    path('api/', include('delivery.urls')),
    path('api/', include('file.urls')),
    path('api/', include('membership_plan.urls')),
    path('api/', include('billing.urls')),
    path('api/', include('finance.urls')),
    path('api/search/', MainSearch.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
