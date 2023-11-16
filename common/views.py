from datetime import date, timedelta
from itertools import dropwhile

from django.http import Http404

from carwash.models import CarWashWorkDay, CarWashRegistration

menu_navigation = [{'title': 'Главная', 'url_name': 'carwash:home'},
                   {'title': 'Доступное время', 'url_name': 'carwash:registration'},
                   {'title': 'Услуги и цены', 'anchor': '#services_price'},
                   {'title': 'Контакты и адрес', 'anchor': '#footer'},
                   ]

FORMATTED_KEY = ['date', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                 '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00',
                 '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']


def create_and_get_week_workday():
    dates_week = [date.today() + timedelta(days=i) for i in range(7)]

    check_objects = CarWashWorkDay.objects.filter(date__in=dates_week).order_by('date')
    if len(check_objects) < 7:
        for day_ in dates_week:  # создаём день (объект CarWashWorkDay), если его нет в БД
            if not CarWashWorkDay.objects.filter(date=day_).exists():
                CarWashWorkDay.objects.create(date=day_)
        check_objects = CarWashWorkDay.objects.filter(date__in=dates_week).order_by('date')

    return check_objects


class Common:
    title = 'Aquamarine'
    menu = range(3)

    @classmethod
    def create_menu(cls, menu):
        for i in menu:
            assert 0 <= i < len(menu_navigation)

        return [menu_navigation[i] for i in menu]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Common, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['menu'] = self.create_menu(self.menu)
        context['staff'] = self.request.user.has_perm('carwash.view_workday')

        return context


def carwash_user_registration_delete(request, registration_pk):
    """
    Функция для UserRegistrationsCancelView и CarWashUserRegistrationAPIView - обработчик события
    'отмены (удаления)' пользователем своей записи
     """
    # user_registration = CarWashRegistration.objects.filter(pk=registration_pk).first()
    #
    # # проверка что пользователь удаляет принадлежащую ему CarWashUserRegistration
    # if not user_registration or user_registration.client != request.user:
    #     raise Http404
    #
    # needed_workday = CarWashWorkDay.objects.get(date=user_registration.date_reg)
    # needed_staff_registration = CarWashRegistration.objects.get(pk=user_registration.carwash_reg.pk)
    # total_time = needed_staff_registration.total_time
    # time_without_sec = str(user_registration.time_reg)[:-3]  # убираем значения секунд во времени записи '10:00'
    #
    # # создаём список времён от времени регистрации user_registration.time_reg и все времена после
    # formatted_key = list(dropwhile(lambda el: el != time_without_sec, FORMATTED_KEY.copy()))
    #
    # # определяем начальный атрибут (time_....) необходимого объекта WorkWay удаляемой "Записи"
    # attr_first_time = 'time_' + formatted_key.pop(0).replace(':', '')
    #
    # # определяем CarWashRegistration в найденном времени-поля, если она есть
    # first_time_registration = getattr(needed_workday, attr_first_time, None)
    #
    # # если в поле CarWashWorkDay вообще присутствует CarWashRegistration
    # # и её клиент соответствует текущему пользователю, то удаляем в этом поле CarWashWorkDay CarWashRegistration,
    # # а затем, в следующих полях сколько требовалось времён-полей под услуги CarWashRegistration
    # if first_time_registration and first_time_registration.client == request.user:
    #     setattr(needed_workday, attr_first_time, None)
    #     # удаляем записи выбранной CarWashRegistration в полях времени,
    #     # сколько она занимает времен объекта CarWashWorkDay - 30 т.к. начальное время мы уже удалили выше
    #     for _ in range(0, total_time - 30, 30):
    #         setattr(needed_workday, 'time_' + formatted_key.pop(0).replace(':', ''),
    #                 None)  # значению поля соотвествующего времени присваиваем значение None (как по умолчанию)
    #     needed_workday.save()
    #
    # # удаляем CarWashUserRegistration пользователя
    # user_registration.delete()
    pass