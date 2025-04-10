from datetime import date, timedelta

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Q
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import FormView, ListView

from carwash.forms import CarWashRequestCallForm
from carwash.models import (CarWashRegistration, CarWashRequestCall,
                            CarWashService, CarWashWorkDay)
from common.utils import (Common, carwash_user_registration_delete,
                          prepare_workdays, FORMATTED_KEY)

from carwash.use_cases.registration_auto_use_cases import RegistrationAutoGetUseCase, RegistrationAutoPostUseCase
from users.permissions import staff_permission


class IndexListView(Common, ListView):
    """
    Представление для показа главной страницы компании
    и прейскуранта на оказание услуг автомоечного комплекса
    """

    template_name = 'carwash/index.html'
    model = CarWashService
    context_object_name = 'services'
    title = 'Aquamarine'
    # menu_tabs = (1, 2, 3)


class RegistrationAutoView(View):
    """
    Представление пользователю выбора услуг автомоечного комплекса, дня и времени,
     для оказания выбранных услуг.
    Авторизованный пользователь имеет возможность самостоятельной записи автомобиля,
     а неавторизованный пользователя возможность запросить звонок администратора для записи автомобиля
    """
    registration_auto_get_use_case = RegistrationAutoGetUseCase()
    registration_auto_post_use_case = RegistrationAutoPostUseCase()

    def get(self, request):
        template_name, context = self.registration_auto_get_use_case.execute(request=request)
        return render(request, template_name=template_name, context=context)

    def post(self, request):
        template_name, context = self.registration_auto_post_use_case.execute(request=request)
        return render(request, template_name=template_name, context=context)


class UserRegistrationsListView(LoginRequiredMixin, Common, ListView):
    """
    Представление для показа пользователю его записей
     на оказание услуг автомоечного комплекса
    """

    model = CarWashRegistration
    template_name = 'carwash/user-registrations.html'
    context_object_name = 'user_registrations'
    title = 'Мои записи'
    menu_tabs = (0, 1)

    def get_queryset(self):
        queryset = super(UserRegistrationsListView, self).get_queryset()

        return queryset.filter(date_reg__gte=date.today(), client=self.request.user).order_by('date_reg', 'time_reg')


class UserRegistrationsCancelView(LoginRequiredMixin, Common, View):
    """Обработчик события 'отмены (удаления)' пользователем своей записи"""

    def get(self, request, registration_pk):
        carwash_user_registration_delete(request, registration_pk)
        redirect_url = reverse('carwash:user_registrations')

        return HttpResponseRedirect(redirect_url)


class StaffDetailView(Common, PermissionRequiredMixin, View):
    """
    Представление для показа сотруднику всех записей клиентов.
    На сегодня, завтра и послезавтра.
    """

    title = 'Менеджер'
    permission_required = staff_permission

    def get(self, request, days_delta=0):
        if days_delta > 2:
            raise Http404

        # проверяем наличие объектов CarWashWorkDay на неделю вперёд, если их нет, то создаём и возвращаем списком
        # создаём список CarWashWorkDay (today, tomorrow, after_tomorrow)
        workday_for_button = prepare_workdays()[:3]
        current_workday = workday_for_button[days_delta]  # текущий CarWashWorkDay
        time_dict = FORMATTED_KEY[1:].copy()

        # получаем список значений всех времен выбранного объекта CarWashWorkDay
        registrations_workday = [
            getattr(current_workday, 'time_' + time_dict.pop(0).replace(':', '')) for _ in range(22)
        ]

        # создаём список list_workday используя значения текущего CarWashWorkDay, где каждый элемент - словарь
        # [{'time':'10:00', 'id': 1, 'client': 'Elon Musk', ..., 'total_cost': 750},
        #  {'time':'10:30', 'id': 1, 'client': 'Elon Musk', ..., 'total_cost': 750},
        #  {'time':'11:00', 'field': 'Свободно', 'free': True},
        #  ...]
        list_registrations_workday = []

        for t, carwash_registration_data in zip(FORMATTED_KEY[1:], registrations_workday):
            if carwash_registration_data:
                res = {'time': t} | carwash_registration_data
            else:
                res = {'time': t, 'field': 'Свободно', 'free': True}

            list_registrations_workday.append(res)

        # создаём список full_list_registrations_workday и заполняем времена необходимые клиенту на выбранные услуги
        # [{'time':'10:00', 'id': 1, 'client': 'Elon Musk', ..., 'total_cost': 750},
        #  {'time':'10:30', 'field': car_model},
        #  {'time':'11:00', 'field': 'Свободно', 'free': True},
        #  ...]
        iterator_list_registrations_workday = iter(list_registrations_workday)
        full_list_registrations_workday = []

        while iterator_list_registrations_workday:
            another_time = next(iterator_list_registrations_workday, 0)
            if another_time == 0:
                break
            full_list_registrations_workday.append(another_time)  # добавляем в список значение времени CarWashWorkDay
            # в остальные времена добавляем марку автомобиля если это запись пользователя
            if 'id' in another_time:
                car_model = another_time['car_model']
                for i in range(0, another_time['total_time'] - 30, 30):
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
            'staff': request.user.has_perm(staff_permission),
            'button_date': {'today': workday_for_button[0].date,
                            'tomorrow': workday_for_button[1].date,
                            'after_tomorrow': workday_for_button[2].date,
                            },
            'days_delta': days_delta,
            'request_calls': requests_calls,
            'attention': attention,
        }

        return render(request, 'carwash/staff.html', context=context)


class StaffCancelRegistrationView(Common, PermissionRequiredMixin, View):
    """Обработчик события 'отмена (удаление)' сотрудником записи клиента"""

    permission_required = staff_permission

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
    menu_tabs = (0, 1)

    def form_valid(self, form):
        call_me = CarWashRequestCall(phone_number=form.cleaned_data['phone_number'])
        call_me.save()

        context = {
            'title': self.title,
            'menu': self.create_menu((0, 1)),
            'staff': self.request.user.has_perm(staff_permission),
        }

        return render(self.request, 'carwash/request-call-done.html', context=context)


class RequestCallProcessingView(View):
    """Обработчик события 'обработка звонка'"""

    permission_required = staff_permission

    def get(self, request, days_delta, call_pk):
        processed_call = CarWashRequestCall.objects.get(pk=call_pk)
        processed_call.processed = True
        processed_call.save()
        redirect_url = reverse('carwash:staff', kwargs={'days_delta': days_delta})

        return HttpResponseRedirect(redirect_url)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
