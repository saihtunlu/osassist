from django.urls import path
from . import views

urlpatterns = [
    path('deliveries/', views.Deliveries.as_view()),
    path('delivery/', views.SingleDelivery.as_view()),
    path('search-delivery/', views.SearchDelivery.as_view()),
    path('all-deliveries/', views.AllDeliveries.as_view()),

    path('delivery/<int:id>', views.SingleDelivery.as_view()),
    path('remove-deliveries/', views.RemoveMultiDeliveries.as_view()),
]
