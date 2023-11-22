"""Определяет схемы URL для api"""

from django.urls import path

from .views import (CarWashRegistrationAPIView,
                    CarWashRequestCallCreateAPIView, CarWashServiceListAPIView,
                    UserProfileDetailAPIView, UserRegistrationListAPIView)

app_name = 'api'

urlpatterns = [
    path('v1/service-list/', CarWashServiceListAPIView.as_view(), name='service_list'),
    path('v1/carwash-registration/', CarWashRegistrationAPIView.as_view(), name='carwash_registration'),
    path('v1/carwash-user-registration-list/', UserRegistrationListAPIView.as_view(), name='user_registration_list'),
    path('v1/carwash-user-registration-list/<int:registration_pk>/', UserRegistrationListAPIView.as_view(),
         name='user_registration_delete'),
    path('v1/carwash-request-call/', CarWashRequestCallCreateAPIView.as_view(), name='carwash_request_call'),
    path('v1/user-profile/', UserProfileDetailAPIView.as_view(), name='user_profile'),
]
