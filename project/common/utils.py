from datetime import date, timedelta

from django.http import Http404

from carwash.models import CarWashRegistration, CarWashWorkDay


menu_navigation = [{'title': 'Главная', 'url_name': 'carwash:home'},
                   {'title': 'Доступное время', 'url_name': 'carwash:registration'},
                   {'title': 'Услуги и цены', 'anchor': '#services_price'},
                   {'title': 'Контакты и адрес', 'anchor': '#footer'},
                   ]

FORMATTED_KEY = ['date', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                 '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00',
                 '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']

def prepare_workdays():
    """Функция проверяет создание объектов CarWashWorkDay на неделю вперёд
    и в случае их отсутствия создаёт необходимые экземпляры.
    Возвращает QuerySet состоящий из этих семи объектов
    Также удаляет объекты CarWashWorkDay старше года"""

    week_dates = [date.today() + timedelta(days=i) for i in range(7)]
    check_objects = CarWashWorkDay.objects.filter(date__in=week_dates).order_by('date')

    if len(check_objects) < 7:
        for day_ in week_dates:  # создаём день (объект CarWashWorkDay), если его нет в БД
            if not CarWashWorkDay.objects.filter(date=day_).exists():
                CarWashWorkDay.objects.create(date=day_)
        check_objects = CarWashWorkDay.objects.filter(date__in=week_dates).order_by('date')

    return check_objects

def delete_old_record():
    # удаляем экземпляры CarWashWorkDay если они старше 1 года
    CarWashWorkDay.objects.filter(date__lt=date.today() - timedelta(days=365)).delete()


class Common:
    title = 'Aquamarine'
    menu_tabs = range(4)

    @classmethod
    def create_menu(cls, menu_tabs: tuple) -> list:
        """Функция создаёт список вкладок меню в header, в зависимости от предстваления
         и прав пользователя. Список собирается из элементов полного списка menu"""
        for i in menu_tabs:
            assert 0 <= i < len(menu_navigation)

        return [menu_navigation[i] for i in menu_tabs]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Common, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['menu'] = self.create_menu(menu_tabs=self.menu_tabs)
        context['staff'] = self.request.user.is_staff

        return context


def carwash_user_registration_delete(request, registration_pk):
    """Функция для UserRegistrationsCancelView и UserRegistrationListAPIView - обработчик
     события 'отмены (удаления)' пользователем своей записи на автомоечный комплекс."""
    user_registration = CarWashRegistration.objects.filter(pk=registration_pk).first()

    # проверка, что пользователь удаляет принадлежащую ему CarWashUserRegistration
    if not user_registration or user_registration.client != request.user:
        raise Http404

    need_workday = CarWashWorkDay.objects.get(date=user_registration.date_reg)
    time_attributes = user_registration.relation_carwashworkday['time_attributes']
    [setattr(need_workday, t_a, None) for t_a in time_attributes]
    need_workday.save()
    user_registration.delete()
