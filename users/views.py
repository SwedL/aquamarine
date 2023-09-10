from django.shortcuts import render
from django.views.generic import UpdateView
from django.contrib.auth.views import LoginView, LogoutView, AuthenticationForm
from django.urls import reverse_lazy

from users.forms import *
from datetime import date, datetime, timedelta
from common.views import Common
from users.models import User


class UserLoginView(Common, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserLoginView, self).get_context_data()
        context['menu'] = self.menu(0)
        context['title'] = 'Авторизация'

        return context


class UserProfileView(Common, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['menu'] = self.menu(0, 1)
        context['title'] = 'Настройка профиля'
        context['staff'] = self.request.user.has_perm('carwash.view_workday')
        return context

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

