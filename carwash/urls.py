"""Определяет схемы URL для carwash"""

from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from carwash.views import *

app_name = 'carwash'

urlpatterns = [
    path('', IndexListView.as_view(), name='home'),
    path('registration/', RegistrationAutoView.as_view(), name='registration'),
    path('request-call-me/', RequestCallFormView.as_view(), name='call_me'),
    path('request-call-done/', RequestCallDoneTemplateView.as_view(), name='request_call_done'),
    path('staff/<int:days_delta>/', StaffDetailView.as_view(), name='staff'),
    path('cancel/<int:days_delta>/<int:registration_pk>/<str:registration_time>/',
         StaffCancelRegistrationView.as_view(), name='cancel'),
    path('user-registrations/', login_required(UserRegistrationsListView.as_view()), name='user_registrations'),
    path('user-reg-cancel/<int:registration_pk>/', login_required(UserRegistrationsCancelView.as_view()),
         name='user_reg_cancel'),
]
