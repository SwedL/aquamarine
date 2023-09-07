"""Определяет схемы URL для carwash"""

from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from carwash.views import *


app_name = 'carwash'

urlpatterns = [
    path('', IndexListView.as_view(), name='home'),
    path('registration/', RegistrationAutoView.as_view(), name='registration'),
    path('staff/<int:days_delta>/', StaffDetailView.as_view(), name='staff'),
    path('cancel/<int:days_delta>/<int:registration_pk>/<str:registration_time>/', CancelRegistrationView.as_view(), name='cancel'),
    path('user_registrations/', login_required(CarwashUserRegistrationsListView.as_view()), name='user_registrations'),
    path('user_reg_cancel/<int:registration_pk>/', UserRegCancelView.as_view(), name='user_reg_cancel'),
    # path('profile/', Profile.as_view(), name='profile'),
    # path('edit-profile/login/', EditUserLogin.as_view(), name='editlogin'),
    # path('edit-profile/pass/', EditUserPass.as_view(), name='editpass'),
]