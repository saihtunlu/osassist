"""URL's for the chat app."""
from django.urls import path

from . import views

urlpatterns = [
    path('order/list/', views.OrdersListView.as_view()),
    path('order/', views.OrderView.as_view()),
]
