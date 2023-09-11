"""Определяет схемы URL для приложения users"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import *


app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    #path('email/', email, name='email'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]