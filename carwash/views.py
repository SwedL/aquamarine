from django.http import HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, time, datetime, timedelta
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from itertools import dropwhile
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

    def formatted_dict(self, day):
        """Функция создаёт словарь, где ключи из списка FORMATTED_KEY, а значения - значения полей WorkDay"""
        day_object = WorkDay.objects.get(date=day)  # объект WorkDay
        lst_day = list(day_object.__dict__.values())[
                  2:]  # получаем список значений словаря WorkDay только дата и времена
        res_dict = {}

        # создаём и заменяем не занятые времена, сегодняшнего дня, время которых прошло, на значения "disabled"
        if lst_day[0] == day.today():
            for num, k in enumerate(self.FORMATTED_KEY):
                if num != 0 and not lst_day[num] and time(*map(int, k.split(':'))) < datetime.now().time():
                    res_dict[k] = 'disable'
                else:
                    res_dict[k] = lst_day[num]
        else:
            return dict((workday_time, value) for workday_time, value in zip(self.FORMATTED_KEY, lst_day))
        return res_dict

    def get(self, request):
        days_list = [date.today() + timedelta(days=i) for i in range(7)]

        for day_ in days_list:  # создаём день (объект WorkDay), если его нет в БД
            if not WorkDay.objects.filter(date=day_):
                WorkDay.objects.create(date=day_)

        # удаляем экземпляры WorkDay если они старше 1 года
        WorkDay.objects.filter(date__lt=date.today() - timedelta(days=365)).delete()

        services = dict([(k, v) for k, v in enumerate(CarWashService.objects.all(), start=1)])
        list_day_dictionaries = [self.formatted_dict(day) for day in days_list]

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
        total_cost = sum(getattr(x, request.user.car_type) for x in choicen_services)

        # проверяем если ранее User создавал такую же "Запись" с теми же услугами, то используем её.
        all_registrations_user = CarWashRegistration.objects.filter(client=request.user)

        for reg in all_registrations_user:
            if choicen_services == list(reg.services.all()):
                new_reg = reg
                break
        else:
            new_reg = CarWashRegistration(client=request.user)  # создаём "Запись" от пользователя
            new_reg.save()
            [new_reg.services.add(s) for s in choicen_services]  # добавляем в "Запись" выбранные услуги

        # вычисляем общее время работ total_time в "Записи" (7,8,9 считается как за одно время 30 мин.)
        total_time = new_reg.total_time

        for_workday_date = date(*map(int, choicen_date.split()))  # дата по которой будем искать экземпляр WorkDay
        current_workday = WorkDay.objects.get(date=for_workday_date)

        # записываем столько времён под авто, сколько необходимо под услуги
        # из списка времен FORMATTED_KEY выбираем от choicen_time и далее
        formatted_key1 = list(dropwhile(lambda el: el != choicen_time, self.FORMATTED_KEY))
        formatted_key2 = formatted_key1.copy()

        # Если время выбранное всё ещё свободно пока пользователь делал свой выбор, то сохраняем "Запись"
        # уже занято пока проходило оформление, то ОШИБКА ЗАПИСИ
        check_free_times = [getattr(current_workday, 'time_' + formatted_key2.pop(0).replace(':', '')) for _ in
                            range(0, total_time, 30)]

        if all([x is None for x in check_free_times]):
            for _ in range(0, total_time, 30):
                setattr(current_workday, 'time_' + formatted_key1.pop(0).replace(':', ''),
                        new_reg)  # в поле соответствующего времени сохраняем "Запись"
            current_workday.save()

            # создаём запись пользователя для отслеживания в "Мои записи"
            for_workday_time = time(*map(int, choicen_time.split(':')))
            CarWashUserRegistration.objects.create(client=request.user,
                                                   date_reg=for_workday_date,
                                                   time_reg=for_workday_time,
                                                   services=new_reg)

        else:
            context = {
                'title': 'Ошибка записи',
                'staff': request.user.has_perm('carwash.view_workday'),
                'menu': self.menu(0, 1),
            }

            return render(request, 'carwash/registration-error.html', context=context)

        normal_format_choicen_date = choicen_date.split()  # создаём список данных из выбранной даты "2023 09 10"
        normal_format_choicen_date.reverse()  # разворачиваем список для удобного вывода информации пользователю

        normal_total_time = f'{total_time // 60} ч.  {total_time - total_time // 60 * 60} мин.'

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

        # получаем список значений всех времен выбранного объекта Workday
        registrations_workday = [getattr(current_workday, 'time_' + formatted_key.pop(0).replace(':', '')) for _ in
                                 range(22)]

        # создаём список записей рабочего дня list_workday
        # [{'time':'10:00', 'registration': CarWashRegistration, 'services': все услуги},]
        # либо [{'time':'10:00', 'client': 'Свободно', 'free': True},]
        list_workday = []
        for t, registration in zip(self.FORMATTED_KEY[1:], registrations_workday):
            if registration:
                res = {'time': t, 'registration': registration, 'registration_pk': registration.pk,
                       'services': ' // '.join([str(s) for s in registration.services.all()])}
            else:
                res = {'time': t, 'client': 'Свободно', 'free': True}

            list_workday.append(res)

        # создаём список result_list_workday и заполняем времена необходимые клиенту на выбранные услуги
        # [{'time':'10:00', 'registration': CarWashRegistration, 'services': все услуги},
        #  {'time':'10:30', 'client': CarWashRegistration.client},
        #  {'time':'11:00', 'client': CarWashRegistration.client},
        #  {'time':'11:30', 'client': 'Свободно', 'free': True}, ...]
        result_list_workday = []
        list_workday_iterator = iter(list_workday)

        while list_workday_iterator:
            another_time = next(list_workday_iterator, 0)
            if another_time == 0:
                break
            result_list_workday.append(another_time)  #
            if 'registration' in another_time:
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

        # создаём список времён от времени регистрации registration_time и все времена после
        formatted_key1 = list(dropwhile(lambda el: el != registration_time,
                                        self.FORMATTED_KEY.copy()))

        # удаляем записи выбранной регистрации в полях времени, сколько она занимает времен объекта WorkDay
        for _ in range(0, total_time, 30):
            setattr(current_workday, 'time_' + formatted_key1.pop(0).replace(':', ''),
                    None)  # поле соотвествующего времени делаем None по умолчанию
        current_workday.save()

        redirect_url = reverse_lazy('carwash:staff', kwargs={'days_delta': days_delta})

        return HttpResponseRedirect(redirect_url)


class CarwashUserRegistrationsListView(Common, ListView):
    model = CarWashUserRegistration
    template_name = 'carwash/user_registrations.html'
    context_object_name = 'user_registrations'

    def get_queryset(self):
        queryset = super(CarwashUserRegistrationsListView, self).get_queryset()
        # удаляем экземпляры CarwashUserRegistrations если они уже не актуальны на сегодняшний день
        queryset.filter(date_reg__lt=date.today(), client=self.request.user).delete()
        return queryset.filter(date_reg__gte=date.today(), client=self.request.user).order_by('date_reg', 'time_reg')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CarwashUserRegistrationsListView, self).get_context_data()
        context['title'] = 'Aquamarine'
        context['menu'] = self.menu(0, 1)
        context['staff'] = self.request.user.has_perm('carwash.view_workday')
        return context


class UserRegCancelView(Common, View):
    def get(self, request, registration_pk):
        user_registration = CarWashUserRegistration.objects.get(pk=registration_pk)
        
        needed_workday = WorkDay.objects.get(date=user_registration.date_reg)
        needed_staff_registration = CarWashRegistration.objects.get(pk=user_registration.services.pk)
        total_time = needed_staff_registration.total_time
        temp = str(user_registration.time_reg)[:-3]

        # создаём список времён от времени регистрации user_registration.time_reg и все времена после
        formatted_key1 = list(dropwhile(lambda el: el != temp,
                                        self.FORMATTED_KEY.copy()))

        # определяем начальный атрибут (time_....) необходимого объекта WorkWay удаляемой "Записи"
        attr_first_time = 'time_' + formatted_key1.pop(0).replace(':', '')
        # определяем "Запись" в найденном времени-поля, если она есть
        first_time_registration = getattr(needed_workday, attr_first_time)

        # если в поле WorkDay вообще присутствует "Запись"
        # и её клиент соответствует текущему пользователю, то удаляем в этом поле WorkDay "Запись",
        # а затем в следующих полях сколько требовалось времён-полей под услуги "Записи"
        if first_time_registration and first_time_registration.client == request.user:
            setattr(needed_workday, attr_first_time, None)
            # удаляем записи выбранной регистрации в полях времени,
            # сколько она занимает времен объекта WorkDay - 30 т.к. начальное время мы уже удалили выше
            for _ in range(0, total_time - 30, 30):
                setattr(needed_workday, 'time_' + formatted_key1.pop(0).replace(':', ''),
                        None)  # поле соотвествующего времени делаем None по умолчанию
            needed_workday.save()

        # удаляем "Запись пользователя"
        user_registration.delete()

        redirect_url = reverse_lazy('carwash:user_registrations')

        return HttpResponseRedirect(redirect_url)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
