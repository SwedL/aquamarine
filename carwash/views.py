from django.http import HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, time, datetime, timedelta
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from itertools import dropwhile
from django.views.generic import TemplateView, ListView, DetailView

from carwash.models import *
from common.views import Common


menu = ['Главная', 'Записаться', 'Услуги и цены', 'Контакты и адрес']


class IndexListView(Common, ListView):
    template_name = 'carwash/index.html'
    title = 'Aquamarine'
    model = CarWashService
    context_object_name = 'services'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexListView, self).get_context_data()
        context['menu'] = self.menu(1, 2, 3) if self.request.user.is_authenticated else self.menu(2, 3)
        context['staff'] = self.request.user.has_perm('carwash.view_workday')
        context['title'] = self.title

        return context


class RegistrationAutoView(Common, View):
    title = 'Запись автомобиля'
    login_url = reverse_lazy('carwash:home')

    def formatted_dict(self, date):
        """Функция создаёт словарь, где ключи из списка FORMATTED_KEY, а значения - значения полей WorkDay"""
        day_object = WorkDay.objects.get(date=date)  # объект WorkDay
        lst_day = list(day_object.__dict__.values())[2:]  # получаем список значений словаря WorkDay только дата и часы
        res_dict = {}

        # создаём и заменяем не занятые времена, сегодняшнего дня время которых прошло, на значения "disabled"
        if lst_day[0] == date.today():
            for num, k in enumerate(self.FORMATTED_KEY):
                if num != 0 and not lst_day[num] and time(*map(int, k.split(':'))) < datetime.now().time():
                    res_dict[k] = 'disable'
                else:
                    res_dict[k] = lst_day[num]
        else:
            return dict((time, value) for time, value in zip(self.FORMATTED_KEY, lst_day))
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
            'title': self.title,
            'menu': self.menu(0),
            'staff': request.user.has_perm('carwash.view_workday'),
            'services': services,
            'list_day_dictionaries': list_day_dictionaries,
        }

        return render(request, 'carwash/registration.html', context=context)

    def post(self, request):
        choicen_date, choicen_time = request.POST['choice_time'].split(',')
        choicen_services_list_pk = list(
            map(lambda i: int(i.split('_')[1]), filter(lambda x: x.startswith('service'), request.POST)))
        choicen_services = [CarWashService.objects.get(pk=s) for s in choicen_services_list_pk]
        # time789 = sum([x for x in choicen_services_list_pk if x in [7, 8, 9]]) // 10   # если выбраны улуги, то время берётся как за одну
        # overal_time = sum([t.process_time for t in choicen_services]) - time789 * 30   # общее время работ
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

        total_time = new_reg.total_time    # вычисляем общее время работ в "Записи" (7,8,9 считается как за одно время 30 мин.)

        for_workday_date = date(*map(int, choicen_date.split()))  # дата по которой будем искать экземпляр WorkDay
        current_workday = WorkDay.objects.get(date=for_workday_date)  # получаем по дате экземпляр WorkDay

        # записываем столько времён под авто, сколько необходимо под услуги.
        formatted_key1 = list(dropwhile(lambda el: el != choicen_time, self.FORMATTED_KEY.copy())) # из списка времен выбираем от choicen_time и далее
        formatted_key2 = formatted_key1.copy()

        # Если время уже занято пока проходило оформление, то ОШИБКА ЗАПИСИ
        check_free_times = [getattr(current_workday, 'time_' + formatted_key2.pop(0).replace(':', '')) for _ in range(0, total_time, 30)]
        if all([x is None for x in check_free_times]):
            for _ in range(0, total_time, 30):
                setattr(current_workday, 'time_' + formatted_key1.pop(0).replace(':', ''), new_reg)  # в поле соотвеств. времени сохраняем "Запись"
            current_workday.save()
        else:
            context = {
                'title': 'Ошибка записи',
                'staff': request.user.has_perm('carwash.view_workday'),
                'menu': self.menu(0, 1),
            }

            return render(request, 'carwash/registration-error.html', context=context)

        normal_format_choicen_date = choicen_date.split()
        normal_format_choicen_date.reverse()

        normal_total_time = f'{total_time//60} ч.  {total_time - total_time // 60 * 60} мин.'

        context = {
            'title': 'Запись зарегистрирована',
            'menu': self.menu(0),
            'staff': request.user.has_perm('carwash.view_workday'),
            'normal_format_choicen_date': '/'.join(normal_format_choicen_date),
            'choice_time': choicen_time,
            'choice_services': choicen_services,
            'total_time': normal_total_time,
            'total_cost': f'{total_cost} р.',
        }

        return render(request, 'carwash/done.html', context=context)


class StaffDetailView(Common, View):
    title = 'Сотрудник'

    def get(self, request, days_delta):
        current_workday = WorkDay.objects.get(date=date.today() + timedelta(days=days_delta))
        formatted_key = self.FORMATTED_KEY[1:].copy()

        registrations_workday = [getattr(current_workday, 'time_' + formatted_key.pop(0).replace(':', '')) for _ in range(22)]

        # создаём список записей рабочего дня [{'time':'10:00', 'registration': CarWashRegistration, 'services': все услуги},]
        list_workday = []
        for t, registration in zip(self.FORMATTED_KEY[1:], registrations_workday):
            if registration:
                res = {'time': t, 'registration': registration, 'registration_pk': registration.pk, 'services': ' // '.join([str(s) for s in registration.services.all()])}
            else:
                res = {'time': t, 'client': 'Свободно', 'free': True}

            list_workday.append(res)

        list_workday_iterator = iter(list_workday)
        result_list_workday = []

        while list_workday_iterator:
            another_time = next(list_workday_iterator, 0)
            if another_time == 0:
                break
            result_list_workday.append(another_time)
            if 'registration' in another_time:
                if len(another_time['services']) > 150:
                    another_time['big'] = True
                total_time_without30 = another_time['registration'].total_time - 30
                for i in range(0, total_time_without30, 30):
                    another_time = next(list_workday_iterator)
                    registration_busy = {'time': another_time['time'], 'client': another_time['registration'].client}
                    result_list_workday.append(registration_busy)

        context = {
            'title': self.title,
            'menu': self.menu(0, 1),
            'list_workday': result_list_workday,
            'staff': True,
            'days_delta': days_delta,
        }

        return render(request, 'carwash/staff.html', context=context)


class CancelRegistrationView(Common, View):
    def get(self, request, days_delta, registration_pk, registration_time):
        current_workday = WorkDay.objects.get(date=date.today() + timedelta(days=days_delta))
        registration = CarWashRegistration.objects.get(pk=registration_pk)
        total_time = registration.total_time

        # создаём список времён от времени регистрации и все времена после неё
        formatted_key1 = list(dropwhile(lambda el: el != registration_time, self.FORMATTED_KEY.copy()))  # из списка времен выбираем от wd_time и далее

        # удаляем записи выбранной регистрации в полях времени, сколько она занимает
        for _ in range(0, total_time, 30):
            setattr(current_workday, 'time_' + formatted_key1.pop(0).replace(':', ''), None)  # в поле соотвеств. времени сохраняем "Запись"
        current_workday.save()

        redirect_url = reverse_lazy('carwash:staff', kwargs={'days_delta': days_delta})  #HttpResponse('<script>history.back();</script>')

        return HttpResponseRedirect(redirect_url)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
