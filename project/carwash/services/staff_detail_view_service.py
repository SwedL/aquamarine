from datetime import timedelta

from django.db.models import Q, QuerySet
from django.http import Http404
from django.utils import timezone

from carwash.models import CarWashRequestCall
from common.utils import FORMATTED_KEY, Common
from users.models import User


class StaffDetailViewService(Common):
    def get_context(self, user: User, days_delta: int, week_workday_objects: QuerySet) -> dict:
        if days_delta > 2:
            raise Http404

        current_workday = week_workday_objects[days_delta]  # текущий CarWashWorkDay
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
        registrations_workday_list = []

        for t, carwash_registration_data in zip(FORMATTED_KEY[1:], registrations_workday):
            if carwash_registration_data:
                res = {'time': t} | carwash_registration_data
            else:
                res = {'time': t, 'field': 'Свободно', 'free': True}
            registrations_workday_list.append(res)

        # создаём список full_list_registrations_workday и заполняем времена необходимые клиенту на выбранные услуги
        # [{'time':'10:00', 'id': 1, 'client': 'Elon Musk', ..., 'total_cost': 750},
        #  {'time':'10:30', 'field': car_model},
        #  {'time':'11:00', 'field': 'Свободно', 'free': True},
        #  ...]
        registrations_workday_iterator = iter(registrations_workday_list)
        full_registrations_workday_list = []

        while registrations_workday_iterator:
            another_time = next(registrations_workday_iterator, 0)
            if another_time == 0:
                break
            full_registrations_workday_list.append(another_time)  # добавляем в список значение времени CarWashWorkDay
            # в остальные времена добавляем марку автомобиля если это запись пользователя
            if 'id' in another_time:
                car_model = another_time['car_model']
                for i in range(0, another_time['total_time'] - 30, 30):
                    another_time = next(registrations_workday_iterator)
                    registration_busy = {'time': another_time['time'], 'field': car_model}
                    full_registrations_workday_list.append(registration_busy)

        # показываем заказанные звонки, в течение 24 часов
        datetime_now = timezone.now()
        time_1_day_ago = datetime_now - timedelta(days=1)
        requests_calls = CarWashRequestCall.objects.filter(Q(created__gt=time_1_day_ago) & Q(created__lte=datetime_now))
        attention = requests_calls.filter(processed=False)  # переменная указывающая на необработанные звонки

        context = {
            'menu': self.create_menu((0, 1)),
            'full_list_registrations_workday': full_registrations_workday_list,
            'staff': user.is_staff,
            'button_date': {'today': week_workday_objects[0].date,
                            'tomorrow': week_workday_objects[1].date,
                            'after_tomorrow': week_workday_objects[2].date,
                            },
            'days_delta': days_delta,
            'request_calls': requests_calls,
            'attention': attention,
        }

        return context
