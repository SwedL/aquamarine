"""Определяет схемы URL для carwash"""

from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from carwash.views import *


app_name = 'carwash'

urlpatterns = [
    path('', IndexListView.as_view(), name='home'),
    path('registration/', RegistrationAutoView.as_view(), name='registration'),
    path('registration/call_me/', RequestCallFormView.as_view(), name='call_me'),
    path('staff/<int:days_delta>/', StaffDetailView.as_view(), name='staff'),
    path('cancel/<int:days_delta>/<int:registration_pk>/<str:registration_time>/', StaffCancelRegistrationView.as_view(), name='cancel'),
    path('user_registrations/', login_required(UserRegistrationsListView.as_view()), name='user_registrations'),
    path('user_reg_cancel/<int:registration_pk>/', UserRegistrationsCancelView.as_view(), name='user_reg_cancel'),
]