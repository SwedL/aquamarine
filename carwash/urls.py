"""Определяет схемы URL для carwash"""

from django.urls import path
from carwash.views import *

app_name = 'carwash'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('registration/', RegistrationAuto.as_view(), name='registration'),
    # path('profile/', Profile.as_view(), name='profile'),
    # path('login/', LoginUser.as_view(), name='login'),
    # path('logout/', logout_user, name='logout'),
    # path('edit-profile/login/', EditUserLogin.as_view(), name='editlogin'),
    # path('edit-profile/pass/', EditUserPass.as_view(), name='editpass'),
]