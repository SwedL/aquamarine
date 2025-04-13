from datetime import date, time
from itertools import dropwhile

from django.core.handlers.asgi import ASGIRequest
from django.db import transaction
from django.db.models import QuerySet

from carwash.exceptions.exceptions import TimeAlreadyTakenException
from carwash.models import CarWashRegistration, CarWashService, CarWashWorkDay
from carwash.services.validators import FreeTimeCarWashWorkDayValidatorService
from common.utils import FORMATTED_KEY, Common


class RegistrationAutoPostService(Common):
    free_time_validator = FreeTimeCarWashWorkDayValidatorService
    template_name_done = 'carwash/registration-done.html'
    template_name_error = 'carwash/registration-error.html'

    def create_registration(self, request: ASGIRequest) -> tuple[str, dict]:
        selected_date, selected_time = request.POST['choice_date_and_time'].split(',')
        selected_service_ids = list(
            map(lambda i: int(request.POST[i]), filter(lambda x: x.startswith('service'), request.POST))
        )
        selected_services = CarWashService.objects.filter(pk__in=selected_service_ids)

        total_cost = sum(getattr(x, request.user.car_type) for x in selected_services)

        select_workday_date = date(*map(int, selected_date.split()))  # дата, которую выбрал клиент
        select_workday_time = time(*map(int, selected_time.split(':')))  # время, которое выбрал клиент

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
                # добавляем в CarWashRegistration выбранные услуги
                new_registration.services.set(selected_services)
                # получаем данные CarWashRegistration в виде словаря
                new_registration_data = new_registration.get_data()
                # если записывает сотрудник, то берутся данные 'comment_...'
                match request.POST:
                    case {
                        'comment_car_model': car_model,
                        'comment_phone_number': phone_number,
                        'comment_client': client,
                    }:
                        new_registration_data['car_model'] = car_model
                        new_registration_data['phone_number'] = phone_number
                        new_registration_data['client'] = client

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

                # создаём список данных из выбранной даты "2023 09 10"
                normal_format_selected_date = selected_date.split()
                # разворачиваем список для удобного вывода информации пользователю
                normal_format_selected_date.reverse()

                normal_total_time = f'{total_time // 60} ч.  {total_time - total_time // 60 * 60} мин.'

                context = {
                    'title': 'Запись зарегистрирована',
                    'menu': self.create_menu((0,)),
                    'staff': request.user.is_staff,
                    'normal_format_selected_date': '/'.join(normal_format_selected_date),
                    'choice_time': selected_time,
                    'choice_services': selected_services,
                    'total_time': normal_total_time,
                    'total_cost': f'{total_cost} р.',
                }

                if request.user.is_staff:
                    context.get('menu').append({'title': 'Менеджер', 'url_name': 'carwash:staff'})

                return self.template_name_done, context

        except TimeAlreadyTakenException:
            context = {
                'title': 'Ошибка записи',
                'menu': self.create_menu((0, 1)),
                'staff': request.user.is_staff,
            }
            return self.template_name_error, context

    def get_total_time(self, selected_services: QuerySet) -> int:
        """
        Вычисляем общее время работ total_time в CarWashRegistration
         (id работ [7,8,9] считается как за одно время 30 мин.)
        """
        time789 = sum([x.pk for x in selected_services if x.pk in [7, 8, 9]]) // 10
        total_time = sum([t.process_time for t in selected_services]) - time789 * 30
        return total_time
