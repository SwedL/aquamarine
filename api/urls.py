"""Определяет схемы URL для carwash"""

from django.urls import path, include
from rest_framework import routers

from api.views import *

app_name = 'api'

# router = routers.DefaultRouter()
# router.register(r'carwashuserregistration', CarWashUserRegistrationListAPIView)

urlpatterns = [
    path('v1/service-list/', CarWashServiceListAPIView.as_view(), name='service_list'),
    path('v1/carwash-request-call/', CarWashRequestCallCreateAPIView.as_view(), name='carwash_request_call'),
    path('v1/carwash-user-registration-list/', CarWashUserRegistrationAPIView.as_view()),
    path('v1/carwash-user-registration-list/<int:registration_pk>/', CarWashUserRegistrationAPIView.as_view()),
    path('v1/carwash-registration/', CarWashRegistrationAPIView.as_view()),
    # path('v1/', include(router.urls)),
]
