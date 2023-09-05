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


class UserRegistrationsView(Common, View):

    def get(self, request):
        actual_days = WorkDay.objects.filter(date__gte=datetime.today())
        user_registrations = []

        for current_workday in actual_days:
            # получаем список значений всех времен выбранного текущего объекта Workday
            registrations_current_workday = [(current_workday.date, time_, getattr(current_workday, 'time_' + time_.replace(':', ''))) for time_ in self.FORMATTED_KEY[1:]]

            # выбираем в список user_registrations Записи текущего пользователя
            [user_registrations.append((cwd, time_, reg)) for cwd, time_, reg in registrations_current_workday if reg and reg.client == request.user]

        context = {
            'title': 'Aquamarine',
            'user_registrations': user_registrations,
            'menu': self.menu(0),
        }

        return render(request, 'users/user_registrations.html', context=context)

# class UserRegistrationsView(Common, ListView):
#     model = WorkDay
#     template_name = 'users/user_registrations.html'
#     context_object_name = 'workdays'
#
#     def get_queryset(self):
#         queryset = super(UserRegistrationsView, self).get_queryset()
#         return queryset.filter(date__gte=datetime.today())
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(UserRegistrationsView, self).get_context_data()
#         context['title'] = 'Aquamarine'
#         context['categories'] = ProductCategory.objects.all()
#         return context
#     pass
