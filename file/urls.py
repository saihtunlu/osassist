from django.urls import path
from . import views

urlpatterns = [
    path('files/', views.Files.as_view()),
    path('file/', views.SingleFile.as_view()),
    path('remove-files/', views.RemoveFiles.as_view()),

]
