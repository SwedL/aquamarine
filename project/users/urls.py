"""Определяет схемы URL для приложения users"""

from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import (PasswordChangeDoneTemplateView,
                         UserForgotPasswordView, UserLoginView,
                         UserPasswordChangeView, UserPasswordResetConfirmView,
                         UserProfileView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneTemplateView.as_view(), name='password_change_done'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
