from django.shortcuts import render
from django.contrib.auth.views import LoginView, AuthenticationForm, LogoutView
from django.urls import reverse_lazy

from users.forms import UserLoginForm
from common.views import Common


class UserLoginView(Common, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserLoginView, self).get_context_data()
        context['menu'] = self.menu(0)

        return context






