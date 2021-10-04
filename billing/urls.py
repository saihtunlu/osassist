from django.urls import path
from . import views

urlpatterns = [
    path('billing/', views.BillingView.as_view()),
    path('payment-methods/', views.PaymentMethodsView.as_view()),
    path('billings/', views.BillingsView.as_view()),
    path('stores-billings/', views.StoresBillingsView.as_view()),
    path('billing-payment/', views.BillingPaymentView.as_view()),
    path('billing-status/', views.BillingStatusView.as_view()),
]
