from django.shortcuts import render
from django.contrib.auth.views import LoginView, AuthenticationForm, LogoutView
from django.urls import reverse_lazy
from users.forms import UserLoginForm


menu = [{'title': 'Главная', 'url_name': 'carwash:home'},
        {'title': 'Записаться', 'url_name': 'carwash:registration'},
        {'title': 'Услуги и цены', 'anchor': '#services_price'},
        {'title': 'Контакты и адрес', 'anchor': '#footer'},
        ]

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm #UserLoginForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserLoginView, self).get_context_data()

        user_menu = menu.copy()
        context['menu'] = [user_menu[0]]

        return context






