from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView, AuthenticationForm
from django.urls import reverse_lazy

from users.forms import UserLoginForm
from datetime import date, datetime, timedelta
from carwash.models import WorkDay
from common.views import Common


class UserLoginView(Common, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserLoginView, self).get_context_data()
        context['menu'] = self.menu(0)

        return context

