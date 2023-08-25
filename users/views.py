from django.shortcuts import render
from django.contrib.auth.views import LoginView, AuthenticationForm, LogoutView
from django.urls import reverse_lazy
from users.forms import UserLoginForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm #UserLoginForm

    # def get_success_url(self):
    #     return reverse_lazy('carwash:home')




