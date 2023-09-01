"""Определяет схемы URL для carwash"""

from django.urls import path
from carwash.views import *


app_name = 'carwash'

urlpatterns = [
    path('', IndexListView.as_view(), name='home'),
    path('registration/', RegistrationAutoView.as_view(), name='registration'),
    path('staff/<int:days_delta>/', StaffDetailView.as_view(), name='staff'),
    path('cancel/<int:days_delta>/<int:registration_pk>/<str:registration_time>/', CancelRegistrationView.as_view(), name='cancel'),
    # path('profile/', Profile.as_view(), name='profile'),
    # path('login/', LoginUser.as_view(), name='login'),
    # path('logout/', logout_user, name='logout'),
    # path('edit-profile/login/', EditUserLogin.as_view(), name='editlogin'),
    # path('edit-profile/pass/', EditUserPass.as_view(), name='editpass'),
]