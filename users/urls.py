"""Определяет схемы URL для приложения users"""
from django.contrib.auth.decorators import login_required
from django.urls import path
from users.views import UserLoginView, UserRegistrationsView, LogoutView  #, AuthenticationForm



app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_registrations/', login_required(UserRegistrationsView.as_view()), name='user_registrations'),
    # path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
]