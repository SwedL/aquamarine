from datetime import date, time
from itertools import dropwhile
from typing import Any

from django.db import transaction
from rest_framework.request import Request

from api.carwash.exceptions.exceptions import TimeAlreadyTakenException
from carwash.models import CarWashService, CarWashRegistration, CarWashWorkDay
from carwash.serializers import CarWashServiceSerializer

FORMATTED_KEY = ['date', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                 '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00',
                 '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']

class FreeTimeCarWashWorkDayValidatorService:
    @staticmethod
    def validate(attributes: dict[str, Any]) -> None:
        """Проверяем свободно ли ещё время пока пользователь делал свой выбор"""

        workday = CarWashWorkDay.objects.filter(date=attributes['date']).first()
        process_times = attributes['process_times']
        total_time = attributes['total_time']
        check_free_times = [getattr(workday, 'time_' + process_times.pop(0).replace(':', '')) for _ in
                            range(0, total_time, 30)]
        if any([x for x in check_free_times]):
            raise TimeAlreadyTakenException()


class APIRegistrationAutoPostService:
    free_time_validator = FreeTimeCarWashWorkDayValidatorService

    def create_registration(self, request: Request) -> dict:
        selected_date, selected_time = request.data['selected_date_and_time'].split(',')
        selected_services = CarWashService.objects.filter(
            pk__in=list(map(int, request.data['services_ids'].split())))

        total_cost = sum(getattr(x, request.user.car_type) for x in selected_services)

        select_workday_date = date(*map(int, selected_date.split()))
        select_workday_time = time(*map(int, selected_time.split(':')))

        # записываем столько времён под авто, сколько необходимо под услуги
        # из списка времен FORMATTED_KEY выбираем от selected_time и далее
        process_times = list(dropwhile(lambda el: el != selected_time, FORMATTED_KEY))
        total_time = self.get_total_time(selected_services=selected_services)

        try:
            with transaction.atomic():
                new_registration = CarWashRegistration.objects.create(
                    client=request.user,
                    date_reg=select_workday_date,
                    time_reg=select_workday_time,
                    total_time=total_time,
                    total_cost=total_cost,
                )
                new_registration.services.set(selected_services)  # добавляем в CarWashRegistration выбранные услуги

                new_registration_data = new_registration.get_data()  # получаем данные CarWashRegistration в виде словаря
                selected_workday = CarWashWorkDay.objects.select_for_update().filter(date=select_workday_date).first()

                self.free_time_validator.validate(attributes={
                    'date': select_workday_date,
                    'process_times': process_times.copy(),
                    'total_time': total_time,
                })

                time_attributes = []
                for _ in range(0, total_time, 30):
                    time_attribute = 'time_' + process_times.pop(0).replace(':', '')
                    time_attributes.append(time_attribute)
                    # в поле соответствующего времени сохраняем JSON объект данных CarWashRegistration
                    setattr(selected_workday, time_attribute, new_registration_data)
                selected_workday.save()
                new_registration.relation_carwashworkday = {'time_attributes': time_attributes}
                new_registration.save()

            context = {'title': 'Запись зарегистрирована',
             'selected_services': CarWashServiceSerializer(selected_services, many=True).data,
             'selected_date': selected_date,
             'selected_time': selected_time,
             'total_time': total_time,
             'total_cost': f'{total_cost} р.',
             }

            return context
        except TimeAlreadyTakenException as e:
            return e.message

    def get_total_time(self, selected_services):
        """
        Вычисляем общее время работ total_time в CarWashRegistration
         (id работ [7,8,9] считается как за одно время 30 мин.)
        """
        time789 = sum([x.pk for x in selected_services if x.pk in [7, 8, 9]]) // 10
        total_time = sum([t.process_time for t in selected_services]) - time789 * 30
        return total_time
