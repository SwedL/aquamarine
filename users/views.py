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


class UserPasswordChangeView(Common, PasswordChangeView):
    model = User
    form_class = MyPasswordChangeForm
    template_name = 'users/password_change.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserPasswordChangeView, self).get_context_data()
        context['menu'] = self.menu(0, 1)
        context['title'] = 'Смена пароля'
        context['staff'] = self.request.user.has_perm('carwash.view_workday')
        return context

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id,))


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """Представление по сбросу пароля по почте"""
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('carwash:home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/password_subject_reset_mail.txt'
    email_template_name = 'users/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    # def post(self, request, *args, **kwargs):
    #     pass


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """Представление установки нового пароля"""
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('carwash:home')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context


# def email(request):
#     send_mail(
#         subject="Subject here",
#         message="Here is the message.",
#         from_email='aquamarine.srv@yandex.ru',
#         recipient_list=["supersega@mail.ru"],
#         fail_silently=False,
#     )
#
#     redirect_url = reverse_lazy('carwash:home')
#
#     return HttpResponseRedirect(redirect_url)

