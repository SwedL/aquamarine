from datetime import date, timedelta

from django.http import Http404

from carwash.models import CarWashRegistration, CarWashWorkDay

menu_navigation = [{'title': 'Главная', 'url_name': 'carwash:home'},
                   {'title': 'Доступное время', 'url_name': 'carwash:registration'},
                   {'title': 'Услуги и цены', 'anchor': '#services_price'},
                   {'title': 'Контакты и адрес', 'anchor': '#footer'},
                   ]


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
        context['staff'] = self.request.user.has_perm('carwash.view_carwashworkday')

        return context


def carwash_user_registration_delete(request, registration_pk):
    """
    Функция для UserRegistrationsCancelView и UserRegistrationListAPIView - обработчик события
    'отмены (удаления)' пользователем своей записи на автомоечный комплекс.
    """
    user_registration = CarWashRegistration.objects.filter(pk=registration_pk).first()

    # проверка что пользователь удаляет принадлежащую ему CarWashUserRegistration
    if not user_registration or user_registration.client != request.user:
        raise Http404

    need_workday = CarWashWorkDay.objects.get(date=user_registration.date_reg)
    time_attributes = user_registration.relation_carwashworkday['time_attributes']
    [setattr(need_workday, t_a, None) for t_a in time_attributes]
    need_workday.save()
    user_registration.delete()
