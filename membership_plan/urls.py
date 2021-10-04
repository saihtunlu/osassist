"""URL's for the chat app."""
from django.urls import path

from . import views

urlpatterns = [
    path('memberships/', views.Plans.as_view()),
    path('membership/', views.PlanView.as_view()),

]
