from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('auth/', views.Auth.as_view()),
    path('users/', views.Users.as_view()),
    path('reset-password/', views.ResetPassword.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),
    path('change-email/', views.ChangeEmail.as_view()),
    path('verify-code/', views.VerifyCode.as_view()),
    path('logout/', views.Logout.as_view()),
    path('login/', views.CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
