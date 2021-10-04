from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.SingleStore.as_view()),
    path('stores/', views.Stores.as_view()),
    path('register-store/', views.RegisterStore.as_view()),

]
