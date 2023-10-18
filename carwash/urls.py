"""Определяет схемы URL для carwash"""

from django.urls import path
from carwash.views import *

app_name = 'carwash'

urlpatterns = [
    path('', IndexListView.as_view(), name='home'),
    path('registration/', RegistrationAutoView.as_view(), name='registration'),
    path('request-call-me/', RequestCallFormView.as_view(), name='call_me'),
    path(
        'request-call-processing/<int:days_delta>/<int:call_pk>/',
        RequestCallProcessingView.as_view(),
        name='request_call_processing',
    ),
    path('staff/<int:days_delta>/', StaffDetailView.as_view(), name='staff'),
    path(
        'cancel/<int:days_delta>/<int:registration_pk>/<str:registration_time>/',
        StaffCancelRegistrationView.as_view(),
        name='cancel',
    ),
    path('user-registrations/', UserRegistrationsListView.as_view(), name='user_registrations'),
    path('user-reg-cancel/<int:registration_pk>/', UserRegistrationsCancelView.as_view(), name='user_reg_cancel'),
]
