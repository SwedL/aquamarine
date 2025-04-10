from datetime import date, timedelta

from django.db.models import QuerySet

from carwash.models import CarWashWorkDay, CarWashService
from users.models import User
from common.utils import Common


class RegistrationAutoGetService(Common):
    template_name = 'carwash/registration.html'

    def get_context(self, user: User, week_workday_objects: QuerySet) -> tuple[str, dict]:
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

        return self.template_name, context



