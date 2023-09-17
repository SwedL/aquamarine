from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


from users.forms import *
from datetime import date, datetime, timedelta
from common.views import Common
from users.models import User


class UserLoginView(Common, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Авторизация'
    menu = (0, )


class UserProfileView(Common, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Настройка профиля'
    menu = (0, 1, )

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class UserPasswordChangeView(Common, PasswordChangeView):
    model = User
    form_class = MyPasswordChangeForm
    template_name = 'users/password_change.html'
    title = 'Смена пароля'
    menu = (0, 1, )

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id,))


class UserForgotPasswordView(Common, SuccessMessageMixin, PasswordResetView):
    """Представление по сбросу пароля по почте"""
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('carwash:home')
    #success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/password_subject_reset_mail.txt'
    email_template_name = 'users/password_reset_mail.html'
    title = 'Запрос на восстановление пароля'
    menu = (0, 1, )


class UserPasswordResetConfirmView(Common, SuccessMessageMixin, PasswordResetConfirmView):
    """Представление установки нового пароля"""
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пароль успешно изменен.\nМожете авторизоваться на сайте.'
    title = 'Установить новый пароль'
    menu = (0, 1, )

