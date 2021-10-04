from django.urls import path
from . import views

urlpatterns = [
    path('sale/', views.SingleSale.as_view()),
    path('sales/', views.Sales.as_view()),
    path('sale-products/', views.SaleProducts.as_view()),
    path('payment/', views.SingleOrderPayment.as_view()),
    path('sale-reports/', views.SaleReport.as_view()),
    path('remove-sale-product/', views.SingleSaleProduct.as_view()),
    path('fulfill/', views.Fulfill.as_view()),
    path('invoice/', views.Invoices.as_view()),
    path('sales-status/', views.SalesStatus.as_view()),
    path('order-products/', views.GetOrderProducts.as_view()),

]
