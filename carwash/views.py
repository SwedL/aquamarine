from datetime import date, time, timedelta
from itertools import dropwhile

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import FormView, ListView

from carwash.forms import CarWashRequestCallForm
from carwash.models import *
from common.views import *

# menu = ['Главная', 'Доступное время', 'Услуги и цены', 'Контакты и адрес']

FORMATTED_KEY = ['date', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                 '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00',
                 '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']


class IndexListView(Common, ListView):
    """
    Представление для показа главной страницы компании
    и прейскуранта цен на оказание услуг автомойки
    """

    template_name = 'carwash/index.html'
    model = CarWashService
    context_object_name = 'services'
    title = 'Aquamarine'
    menu = (1, 2, 3)


class RegistrationAutoView(Common, View):
    """
    Представление для просмотра доступного времени необходимого дня,
    а также записи клиентов на оказание услуг автомойки
    """

    def get(self, request):
        # проверяем наличие объектов CarWashWorkDay на неделю вперёд и получаем их из функции
        objects_week_workday = create_and_get_week_workday()

        # удаляем экземпляры CarWashWorkDay если они старше 1 года
        CarWashWorkDay.objects.filter(date__lt=date.today() - timedelta(days=365)).delete()

        # создаём словарь где ключи это id услуги, а значение, сама услуга
        services = dict([(service.pk, service) for service in CarWashService.objects.all().order_by('id')])

        # получаем список из словарей значений CarWashWorkDay
        # {'date': datetime.date(2023, 10, 24), '10:00': 'disable', '10:30': 3, '11:00': 3, ...}
        # где key - время, value - CarWashRegistration.id либо 'disabled' если время прошло, None если время актуально
        list_day_dictionaries = list(map(lambda i: i.formatted_dict(), objects_week_workday))

        context = {
            'title': 'Запись автомобиля',
            'menu': self.create_menu((0,)),
            'staff': request.user.has_perm('carwash.view_carwashworkday'),
            'services': services,
            'list_day_dictionaries': list_day_dictionaries,
        }

        if request.user.has_perm('carwash.view_carwashworkday'):
            context.get('menu').append({'title': 'Сотрудник', 'url_name': 'carwash:staff'})

        if 'api' in str(request):
            return context

        return render(request, 'carwash/registration.html', context=context)

    def post(self, request):
        choicen_date, choicen_time = request.POST['choice_date_and_time'].split(',')
        choicen_services_list_pk = list(
            map(lambda i: int(request.POST[i]), filter(lambda x: x.startswith('service'), request.POST))
        )
        choicen_services = CarWashService.objects.filter(pk__in=choicen_services_list_pk)
        total_cost = sum(getattr(x, request.user.car_type) for x in choicen_services)

        for_workday_date = date(*map(int, choicen_date.split()))  # дата которую выбрал клиент
        for_workday_time = time(*map(int, choicen_time.split(':')))  # время которое выбрал клиент

        # вычисляем общее время работ total_time в CarWashRegistration (7,8,9 считается как за одно время 30 мин.)
        time789 = sum([x.pk for x in choicen_services if
                       x.pk in [7, 8, 9]]) // 10  # если выбраны улуги, то время берётся как за одну услугу
        total_time = sum([t.process_time for t in choicen_services]) - time789 * 30

        new_reg = CarWashRegistration.objects.create(
                client=request.user,
                date_reg=for_workday_date,
                time_reg=for_workday_time,
                total_time=total_time,
                total_cost=total_cost,
            )
        new_reg.services.set(choicen_services)  # добавляем в CarWashRegistration выбранные услуги
        current_workday = CarWashWorkDay.objects.filter(date=for_workday_date).first()

        # записываем столько времён под авто, сколько необходимо под услуги
        # из списка времен FORMATTED_KEY выбираем от choicen_time и далее
        time_dict1 = list(dropwhile(lambda el: el != choicen_time, FORMATTED_KEY))
        time_dict2 = time_dict1.copy()

        # Если время выбранное всё ещё свободно пока пользователь делал свой выбор,
        # то сохраняем CarWashRegistration, если занято пока проходило оформление,
        # то сообщаем "К сожалению, время которые вы выбрали уже занято"
        check_free_times = [getattr(current_workday, 'time_' + time_dict2.pop(0).replace(':', '')) for _ in
                            range(0, total_time, 30)]

        if all([x is None for x in check_free_times]):
            time_attributes = []
            self_data = new_reg.get_data()  # получаем данные CarWashRegistration в виде словаря
            self_data['car_model'] = request.POST.get('comment_car_model', self_data['car_model'])
            self_data['phone_number'] = request.POST.get('comment_phone_number', self_data['phone_number'])
            if request.POST.get('comment_client', None):
                self_data['client'] = request.POST['comment_client']

            for _ in range(0, total_time, 30):
                time_attribute = 'time_' + time_dict1.pop(0).replace(':', '')
                time_attributes.append(time_attribute)
                # в поле соответствующего времени сохраняем CarWashRegistration
                setattr(current_workday, time_attribute, self_data)
            current_workday.save()
            new_reg.relation_carwashworkday = {'time_attributes': time_attributes}
            new_reg.save()

        else:
            context = {
                'title': 'Ошибка записи',
                'menu': self.create_menu((0, 1)),
                'staff': request.user.has_perm('carwash.view_carwashworkday'),
            }
            if 'api' in str(request):
                return context

            return render(request, 'carwash/registration-error.html', context=context)

        normal_format_choicen_date = choicen_date.split()  # создаём список данных из выбранной даты "2023 09 10"
        normal_format_choicen_date.reverse()  # разворачиваем список для удобного вывода информации пользователю

        normal_total_time = f'{total_time // 60} ч.  {total_time - total_time // 60 * 60} мин.'

        context = {
            'title': 'Запись зарегистрирована',
            'menu': self.create_menu((0,)),
            'staff': request.user.has_perm('carwash.view_carwashworkday'),
            'normal_format_choicen_date': '/'.join(normal_format_choicen_date),
            'choice_time': choicen_time,
            'choice_services': choicen_services,
            'total_time': normal_total_time,
            'total_cost': f'{total_cost} р.',
        }

        if request.user.has_perm('carwash.view_carwashworkday'):
            context.get('menu').append({'title': 'Сотрудник', 'url_name': 'carwash:staff'})

        if 'api' in str(request):
            return context
        return render(request, 'carwash/registration-done.html', context=context)


class UserRegistrationsListView(LoginRequiredMixin, Common, ListView):
    """Представление для показа пользователю его записей на оказание услуг автомойки"""

    model = CarWashRegistration
    template_name = 'carwash/user-registrations.html'
    context_object_name = 'user_registrations'
    title = 'Мои записи'
    menu = (0, 1)

    def get_queryset(self):
        queryset = super(UserRegistrationsListView, self).get_queryset()

        # удаляем экземпляры CarwashRegistrations если они уже не актуальны на сегодняшний день
        queryset.filter(date_reg__lt=date.today(), client=self.request.user).delete()

        return queryset.filter(date_reg__gte=date.today(), client=self.request.user).order_by('date_reg', 'time_reg')


class UserRegistrationsCancelView(LoginRequiredMixin, Common, View):
    """Обработчик события 'отмены (удаления)' пользователем своей записи"""

    def get(self, request, registration_pk):
        carwash_user_registration_delete(request, registration_pk)
        redirect_url = reverse('carwash:user_registrations')

        return HttpResponseRedirect(redirect_url)


class StaffDetailView(Common, PermissionRequiredMixin, View):
    """
    Представление для показа сотруднику всех записей клиентов
    на оказание услуг автомойки. На сегодня, завтра и послезавтра.
    """

    title = 'Сотрудник'
    permission_required = 'carwash.view_carwashworkday'

    def get(self, request, days_delta=0):
        if days_delta > 2:
            raise Http404

        # проверяем наличие объектов CarWashWorkDay на неделю вперёд, если их нет, то создаём и возвращаем списком
        # создаём список CarWashWorkDay (today, tomorrow, after_tomorrow)
        workday_for_button = create_and_get_week_workday()[:3]
        current_workday = workday_for_button[days_delta]  # текущий CarWashWorkDay
        time_dict = FORMATTED_KEY[1:].copy()

        # получаем список значений всех времен выбранного объекта CarWashWorkDay
        registrations_workday = [
            getattr(current_workday, 'time_' + time_dict.pop(0).replace(':', '')) for _ in range(22)
        ]

        # создаём список list_workday используя значения текущего CarWashWorkDay, где каждый элемент - словарь
        # [{'time':'10:00', 'registration': CarWashRegistration, 'services': все услуги},]
        # либо [{'time':'10:00', 'client': 'Свободно', 'free': True},]
        list_registrations_workday = []
        for t, carwash_registration_data in zip(FORMATTED_KEY[1:], registrations_workday):
            if carwash_registration_data:
                res = {'time': t,
                       'id': carwash_registration_data['id'],
                       'client': carwash_registration_data['client'],
                       'email': carwash_registration_data['email'],
                       'phone_number': carwash_registration_data['phone_number'],
                       'car_model': carwash_registration_data['car_model'],
                       'services': carwash_registration_data['services'],
                       'total_time': carwash_registration_data['total_time'],
                       'total_cost': carwash_registration_data['total_cost'],
                       }
            else:
                res = {'time': t, 'field': 'Свободно', 'free': True}

            list_registrations_workday.append(res)

        # создаём список full_list_registrations_workday и заполняем времена необходимые клиенту на выбранные услуги
        # [{'time':'10:00', 'id': 1, 'client': user@mail.ru, ..., 'total_cost': 750},
        #  {'time':'10:30', 'field': user@mail.ru},
        #  {'time':'11:00', 'field': 'Свободно', 'free': True},
        #  ...]
        iterator_list_registrations_workday = iter(list_registrations_workday)
        full_list_registrations_workday = []

        while iterator_list_registrations_workday:
            another_time = next(iterator_list_registrations_workday, 0)
            if another_time == 0:
                break
            full_list_registrations_workday.append(another_time)  # добавляем в список значение времени CarWashWorkDay
            if 'id' in another_time:
                total_time_without30 = another_time['total_time'] - 30
                car_model = another_time['car_model']
                for i in range(0, total_time_without30, 30):
                    another_time = next(iterator_list_registrations_workday)
                    registration_busy = {'time': another_time['time'], 'field': car_model}
                    full_list_registrations_workday.append(registration_busy)

        # показываем заказанные звонки, в течении 24 часов
        datetime_now = timezone.now()
        time_1_day_ago = datetime_now - timedelta(days=1)
        requests_calls = CarWashRequestCall.objects.filter(Q(created__gt=time_1_day_ago) & Q(created__lte=datetime_now))
        attention = requests_calls.filter(processed=False)  # переменная указывающая на необработанные звонки

        context = {
            'title': self.title,
            'menu': self.create_menu((0, 1)),
            'full_list_registrations_workday': full_list_registrations_workday,
            'staff': request.user.has_perm('carwash.view_carwashworkday'),
            'button_date': {'today': workday_for_button[0].date,
                            'tomorrow': workday_for_button[1].date,
                            'after_tomorrow': workday_for_button[2].date,
                            },
            'days_delta': days_delta,
            'request_calls': requests_calls,
            'attention': attention,
        }

        return render(request, 'carwash/staff.html', context=context)
    pass


class StaffCancelRegistrationView(Common, PermissionRequiredMixin, View):
    """Обработчик события 'отмена (удаление)' сотрудником записи клиента"""

    permission_required = 'carwash.view_carwashworkday'

    def get(self, request, days_delta, registration_id):
        need_carwash_registration = CarWashRegistration.objects.filter(id=registration_id).first()
        need_workday = CarWashWorkDay.objects.get(date=need_carwash_registration.date_reg)
        time_attributes = need_carwash_registration.relation_carwashworkday['time_attributes']

        # удаляем записи выбранной CarWashRegistration в полях времени CarWashWorkDay,
        # значению поля соответствующего времени присваиваем значение None (как по умолчанию)
        [setattr(need_workday, t_a, None) for t_a in time_attributes]
        need_workday.save()

        redirect_url = reverse('carwash:staff', kwargs={'days_delta': days_delta})

        return HttpResponseRedirect(redirect_url)


class RequestCallFormView(Common, FormView):
    """Представление для заказа звонка клиенту"""

    form_class = CarWashRequestCallForm
    template_name = 'carwash/request-call.html'
    title = 'Заказ звонка'
    menu = (0, 1)

    def form_valid(self, form):
        call_me = CarWashRequestCall(phone_number=form.cleaned_data['phone_number'])
        call_me.save()

        context = {
            'title': self.title,
            'menu': self.create_menu((0, 1)),
            'staff': self.request.user.has_perm('carwash.view_carwashworkday'),
        }

        return render(self.request, 'carwash/request-call-done.html', context=context)


class RequestCallProcessingView(View):
    """Обработчик события 'обработка звонка'"""

    permission_required = 'carwash.view_carwashworkday'

    def get(self, request, days_delta, call_pk):
        processed_call = CarWashRequestCall.objects.get(pk=call_pk)
        processed_call.processed = True
        processed_call.save()
        redirect_url = reverse('carwash:staff', kwargs={'days_delta': days_delta})

        return HttpResponseRedirect(redirect_url)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
