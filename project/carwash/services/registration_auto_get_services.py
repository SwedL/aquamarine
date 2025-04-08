from datetime import date, timedelta

from django.db.models import QuerySet

from carwash.models import CarWashWorkDay, CarWashService
from users.models import User
from common.views import Common


class RegistrationAutoGetService(Common):
    def get_context(self, user: User, week_workday_objects: QuerySet) -> dict:
        # создаём словарь, где ключи это id услуги, а значение, сама услуга
        services = dict([(service.pk, service) for service in CarWashService.objects.all().order_by('id')])

        list_day_dictionaries = list(map(lambda i: i.formatted_dict(), week_workday_objects))

        context = {
            'title': 'Запись автомобиля',
            'menu': self.create_menu((0,)),
            'staff': user.has_perm('carwash.view_carwashworkday'),
            'services': services,
            'list_day_dictionaries': list_day_dictionaries,
        }

        if user.has_perm('carwash.view_carwashworkday'):
            context.get('menu').append({'title': 'Менеджер', 'url_name': 'carwash:staff'})

        return context


class CreateWeekWorkdayService:
    @staticmethod
    def prepare_workdays():
        """Функция проверяет создание объектов CarWashWorkDay на неделю вперёд
        и в случае их отсутствия создаёт необходимые экземпляры.
        Возвращает QuerySet состоящий из этих семи объектов
        Также удаляет объекты CarWashWorkDay старше года"""

        # удаляем экземпляры CarWashWorkDay если они старше 1 года
        CarWashWorkDay.objects.filter(date__lt=date.today() - timedelta(days=365)).delete()

        dates_week = [date.today() + timedelta(days=i) for i in range(7)]
        check_objects = CarWashWorkDay.objects.filter(date__in=dates_week).order_by('date')

        if len(check_objects) < 7:
            for day_ in dates_week:  # создаём день (объект CarWashWorkDay), если его нет в БД
                if not CarWashWorkDay.objects.filter(date=day_).exists():
                    CarWashWorkDay.objects.create(date=day_)
            check_objects = CarWashWorkDay.objects.filter(date__in=dates_week).order_by('date')

        return check_objects
