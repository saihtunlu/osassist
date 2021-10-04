from django.urls import path
from . import views

urlpatterns = [
    path('suppliers/', views.Suppliers.as_view()),
    path('search-suppliers/', views.SearchSupplier.as_view()),
    path('supplier/', views.SingleSupplier.as_view()),
    path('supplier/<int:id>', views.SingleSupplier.as_view()),
    path('remove-suppliers/', views.RemoveMultiSuppliers.as_view()),
]
