from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView, TemplateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from users.forms import *
from datetime import date, datetime, timedelta
from common.views import Common
from users.models import User


class UserLoginView(Common, LoginView):
    """Представление для авторизации пользователя"""

    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Авторизация'
    menu = (0,)


class UserProfileView(LoginRequiredMixin, Common, UpdateView):
    """Представление отображения профиля пользователя"""

    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Настройка профиля'
    menu = (0, 1,)

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(Common, PasswordChangeView):
    """Представление для смены пароля пользователя"""

    model = User
    form_class = MyPasswordChangeForm
    template_name = 'users/password-change.html'
    title = 'Смена пароля'
    menu = (0, 1,)

    def get_success_url(self):
        return reverse('users:password_change_done')


class UserForgotPasswordView(Common, SuccessMessageMixin, PasswordResetView):
    """Представление для сброса пароля пользователя, с помощью эл.почты"""

    form_class = UserForgotPasswordForm
    template_name = 'users/user-password-reset.html'
    success_url = reverse_lazy('carwash:home')
    subject_template_name = 'email/password_subject_reset_mail.txt'
    email_template_name = 'email/password_reset_mail.html'
    title = 'Запрос на сброс пароля'
    menu = (0, 1,)


class UserPasswordResetConfirmView(Common, SuccessMessageMixin, PasswordResetConfirmView):
    """Представление для установки нового пароля пользователя, после утери"""

    form_class = UserSetNewPasswordForm
    template_name = 'users/user-password-set-new.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пароль успешно изменен.\nМожете авторизоваться на сайте.'
    title = 'Установка нового пароля'
    menu = (0, 1,)


class PasswordChangeDoneTemplateView(Common, TemplateView):
    """Представление для подтверждения успешной смены пароля пользователя"""

    template_name = 'users/password-change-done.html'
    menu = (0, 1,)
