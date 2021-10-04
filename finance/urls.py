from django.urls import path
from . import views

urlpatterns = [
    path('finances/', views.Finances.as_view()),
    path('labels/', views.Labels.as_view()),
    path('finance/', views.SingleFinance.as_view()),
    path('finance-report/', views.FinanceReport.as_view()),
    path('remove-finances/', views.RemoveMultiFinance.as_view()),
]
