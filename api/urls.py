"""Определяет схемы URL для carwash"""

from django.urls import path

from api.views import CarWashServiceListAPIView

app_name = 'api'

urlpatterns = [
    path('services-list/', CarWashServiceListAPIView.as_view(), name='services_list'),
]
