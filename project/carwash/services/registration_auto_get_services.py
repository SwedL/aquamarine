from django.db.models import QuerySet

from carwash.models import CarWashService
from common.utils import Common
from users.models import User


class RegistrationAutoGetService(Common):
    template_name = 'carwash/registration.html'

    def get_context(self, user: User, week_workday_objects: QuerySet) -> tuple[str, dict]:
        # создаём словарь, где ключи это id услуги, а значение, сама услуга
        services = dict([(service.pk, service) for service in CarWashService.objects.all().order_by('id')])

        list_day_dictionaries = list(map(lambda i: i.formatted_dict(), week_workday_objects))

        context = {
            'title': 'Запись автомобиля',
            'menu': self.create_menu((0,)),
            'staff': user.is_staff,
            'services': services,
            'list_day_dictionaries': list_day_dictionaries,
        }

        if user.is_staff:
            context.get('menu').append({'title': 'Менеджер', 'url_name': 'carwash:staff'})

        return self.template_name, context
