"""URL's for the chat app."""
from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.OrdersListView.as_view()),
    path('order/', views.OrderView.as_view()),
    path('order-view/', views.OrdersView.as_view()),

]
