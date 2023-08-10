from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

menu = [{'title': 'Главная', 'url_name': 'home'},
        {'title': 'Записаться на услуги', 'url_name': 'registration'},
        {'title': 'Наш адрес', 'url_name': 'home'},
        {'title': 'Личный кабинет', 'url_name': 'profile'},
        ]


class IndexView(TemplateView):
    template_name = 'carwash/index.html'


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
