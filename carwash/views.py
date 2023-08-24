from django.http import HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, time, datetime, timedelta
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from itertools import dropwhile
from django.views.generic import TemplateView, ListView

from carwash.models import *
import locale

menu = [{'title': 'Главная', 'url_name': 'carwash:home'},
        {'title': 'Записаться', 'url_name': 'carwash:registration'},
        {'title': 'Услуги и цены', 'anchor': '#services_price'},
        {'title': 'Контакты и адрес', 'anchor': '#footer'},
        ]


class IndexListView(ListView):
    template_name = 'carwash/index.html'
    model = CarWashService
    context_object_name = 'services'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexListView, self).get_context_data()

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['list_s'] = [i for i in range(0, 100, 2)]
        return context


class RegistrationAuto(LoginRequiredMixin, View):
    FORMATTED_KEY = ['date', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                     '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00',
                     '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30'
                     ]

    login_url = reverse_lazy('carwash:home')

    def formatted_dict(self, date):
        """Функция создаёт словарь, где ключи из списка FORMATTED_KEY, а значения - значения полей WorkDay"""
        day_object = WorkDay.objects.get(date=date)  # объект WorkDay
        lst_day = list(day_object.__dict__.values())[2:]  # получаем список значений словаря WorkDay только дата и часы
        res_dict = {}

        # создаём и заменяем не занятые времена, сегодняшнего дня время которых прошло, на значения "disabled"
        for num, k in enumerate(self.FORMATTED_KEY):
            if lst_day[0] == date.today() and num != 0 and not lst_day[num] and time(*map(int, k.split(':'))) < datetime.now().time():
                res_dict[k] = 'disable'
            else:
                res_dict[k] = lst_day[num]
        return res_dict

    def get(self, request):
        days_list = [date.today() + timedelta(days=i) for i in range(7)]

        for day in days_list:  # создаём день (объект WorkDay), если его нет в БД
            if not WorkDay.objects.filter(date=day):
                WorkDay.objects.create(date=day)

        # Удаляем экземпляры WorkDay если они старше 1 года
        WorkDay.objects.filter(date__lt=date.today() - timedelta(days=365)).delete()

        services = dict([(k, v) for k, v in enumerate(CarWashService.objects.all(), start=1)])
        list_day_dictionaries = [self.formatted_dict(d) for d in days_list]

        context = {
            'title': 'Запись автомобиля',
            'services': services,
            'list_day_dictionaries': list_day_dictionaries,
            'menu': menu,
        }

        return render(request, 'carwash/registration.html', context=context)

    def post(self, request):
        choicen_date, choicen_time = request.POST['choice_time'].split(',')
        choicen_services_list_pk = list(
            map(lambda i: int(i.split('_')[1]), filter(lambda x: x.startswith('service'), request.POST)))
        choicen_services = [CarWashService.objects.get(pk=s) for s in choicen_services_list_pk]
        time789 = sum([x for x in choicen_services_list_pk if x in [7, 8, 9]]) // 10   # если выбраны улуги, то время берётся как за одну
        overal_time = sum([t.process_time for t in choicen_services]) - time789 * 30   # общее время работ
        total_cost = sum(getattr(x, request.user.car_type) for x in choicen_services)


        # Проверяем если ранее user создавал такую же "Запись" с теми же услугами, то используем её.
        all_registrations_user = CarWashRegistration.objects.filter(client=request.user)

        for reg in all_registrations_user:
            if choicen_services == list(reg.services.all()):
                new_reg = reg
                break
        else:
            new_reg = CarWashRegistration(client=request.user)    # создаём "Запись" от пользователя
            new_reg.save()
            [new_reg.services.add(s) for s in choicen_services]    # добавляем в "Запись" выбранные услуги


        for_workday_date = date(*map(int, choicen_date.split()))  # дата по которой будем искать экземпляр WorkDay
        wd = WorkDay.objects.get(date=for_workday_date)  # получаем по дате экземпляр WorkDay

        # записываем столько времён под авто, сколько необходимо под услуги.
        formatted_key1 = list(dropwhile(lambda el: el != choicen_time, self.FORMATTED_KEY.copy())) # из списка времен выбираем от choicen_time и далее
        formatted_key2 = formatted_key1.copy()

        # Если время уже занято пока проходило оформление, то ОШИБКА ЗАПИСИ
        check_free_times = [getattr(wd, 'time_' + formatted_key2.pop(0).replace(':', '')) for _ in range(0, overal_time, 30)]
        if all([x is None for x in check_free_times]):
            for _ in range(0, overal_time, 30):
                setattr(wd, 'time_' + formatted_key1.pop(0).replace(':', ''), new_reg)  # в поле соотвеств. времени сохраняем "Запись"
            wd.save()
        else:
            context = {
                'title': 'Ошибка записи',
                'menu': menu,
            }
            return render(request, 'carwash/registration-error.html', context=context)

        normal_format_choicen_date = choicen_date.split()
        normal_format_choicen_date.reverse()

        normal_overal_time = f'{overal_time//60} ч.  {overal_time - overal_time // 60 * 60} мин.'

        context = {
            'title': 'done',
            'menu': menu,
            'normal_format_choicen_date': '/'.join(normal_format_choicen_date),
            'choice_time': choicen_time,
            'choice_services': choicen_services,
            'overal_time': normal_overal_time,
            'total_cost': f'{total_cost} р.',

        }

        return render(request, 'carwash/done.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
