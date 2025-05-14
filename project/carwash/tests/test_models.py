from datetime import date, time, timedelta

from carwash.models import (CarWashRegistration, CarWashRequestCall,
                            CarWashService, CarWashWorkDay)
from django.test import TestCase
from users.models import User


def calculate_total_time_and_total_cost(registration):
    # вычисляем общее время работ total_time в CarWashRegistration (7,8,9 считается как за одно время 30 мин.)
    choice_services = registration.services.all()
    time789 = sum([x.pk for x in choice_services if
                   x.pk in [7, 8, 9]]) // 10  # если выбраны улуги, то время берётся как за одну услугу
    lst_reg_serv = list(registration.services.all())
    registration.total_time = sum([t.process_time for t in lst_reg_serv]) - time789 * 30
    registration.save()

    registration.total_cost = sum(getattr(x, registration.client.car_type) for x in lst_reg_serv)


class CarWashServiceModelTestCase(TestCase):
    """Тест модели Service"""

    def setUp(self):
        self.service = CarWashService.objects.create(
            name='Мойка (верх, ковры, сушка)',
            process_time=60,
            price_standart=450,
            price_crossover=550,
            price_offroad=650,
        )
        CarWashService.objects.create(
            name='Экспресс-мойка',
            process_time=30,
            price_standart=200,
            price_crossover=200,
            price_offroad=250,
        )
        CarWashService.objects.create(
            name='Экспресс-мойка с шампунем',
            process_time=30,
            price_standart=250,
            price_crossover=250,
            price_offroad=300,
        )

    def test_fields(self):
        # Проверка полей
        service = CarWashService.objects.all().first()
        field_name = service._meta.get_field('name')
        field_process_time = service._meta.get_field('process_time')
        field_price_standart = service._meta.get_field('price_standart')
        field_price_crossover = service._meta.get_field('price_crossover')
        field_price_offroad = service._meta.get_field('price_offroad')

        self.assertEqual(field_name.verbose_name, 'название')
        self.assertEqual(field_name.max_length, 200)
        self.assertEqual(field_process_time.verbose_name, 'длительность')
        self.assertEqual(field_process_time.default, 0)
        self.assertEqual(field_price_standart.verbose_name, 'седан, хетчбэк')
        self.assertEqual(field_price_standart.default, 0)
        self.assertEqual(field_price_crossover.verbose_name, 'кроссовер')
        self.assertEqual(field_price_crossover.default, 0)
        self.assertEqual(field_price_offroad.verbose_name, 'внедорожник')
        self.assertEqual(field_price_offroad.default, 0)

    def test_service_creation(self):
        # Проверка создания объекта CarWashService
        self.assertEqual(self.service.name, 'Мойка (верх, ковры, сушка)')
        self.assertEqual(self.service.process_time, 60)
        self.assertEqual(self.service.price_standart, 450)
        self.assertEqual(self.service.price_crossover, 550)
        self.assertEqual(self.service.price_offroad, 650)

    def test_service_get_all_records(self):
        # Проверка количества созданных объектов модели CarWashService в бд
        self.assertEqual(CarWashService.objects.all().count(), 3)

    def test_service_get_record(self):
        # Проверка получения записи из бд
        carwash = CarWashService.objects.get(name='Мойка (верх, ковры, сушка)')
        self.assertEqual(carwash.process_time, 60)

    def test_service_str(self):
        # Проверка метода __str__()
        self.assertEqual(str(self.service), 'Мойка (верх, ковры, сушка)')

    def test_service_process_time_and_price_default_value(self):
        # Проверка значений по умолчанию объекта CarWashService
        service = CarWashService.objects.create(name='Default Price Service')

        self.assertEqual(service.process_time, 0)
        self.assertEqual(service.price_standart, 0)
        self.assertEqual(service.price_crossover, 0)
        self.assertEqual(service.price_offroad, 0)


class CarWashRegistrationModelTestCase(TestCase):
    """Тест модели CarWashRegistration"""

    fixtures = {'services.json'}

    def setUp(self):
        self.services = CarWashService.objects.all()
        self.user1 = User.objects.create(
            email='testuser@mail.ru',
            password='12345qwerty',
            fio='Иванов Пётр Николаевич',
            phone_number='81234567390',
            car_model='Kia Sportage',
        )
        self.user2 = User.objects.create(email='testuser1@mail.ru', password='12345qwerty')

        self.registration1 = CarWashRegistration.objects.create(
            client=self.user1,
            date_reg=date.today(),
            time_reg=time(10, 00),
        )
        self.registration1.services.set([self.services[0], self.services[6]])
        calculate_total_time_and_total_cost(self.registration1)

        self.registration2 = CarWashRegistration.objects.create(
            client=self.user2,
            date_reg=date.today(),
            time_reg=time(13, 00),
        )
        self.registration2.services.set([self.services[1], self.services[2], self.services[3]])
        calculate_total_time_and_total_cost(self.registration2)

        self.registration789 = CarWashRegistration.objects.create(
            client=self.user2,
            date_reg=date.today(),
            time_reg=time(18, 00),
        )
        self.registration789.services.set([self.services[3], self.services[6], self.services[7], self.services[8]])
        calculate_total_time_and_total_cost(self.registration789)

    def test_fields(self):
        # Проверка полей
        registration = CarWashRegistration.objects.all().first()
        field_client = registration._meta.get_field('client')
        field_services = registration._meta.get_field('services')

        self.assertEqual(field_client.verbose_name, 'клиент')
        self.assertTrue(field_client.many_to_one)
        self.assertIs(field_client.model, CarWashRegistration)
        self.assertEqual(field_services.verbose_name, 'услуги')
        self.assertTrue(field_services.many_to_many)
        self.assertIs(field_services.model, CarWashRegistration)

    def test_registration_get_all_records(self):
        # Проверка количества созданных объектов модели CarWashRegistration в бд
        self.assertEqual(CarWashRegistration.objects.all().count(), 3)

    def test_registration_get_total_time(self):
        # Проверка правильного подсчёта полного времени выбранных услуг Записи (услуги 7,8,9 считаются как за одну)
        registrations = CarWashRegistration.objects.filter(client=self.user2)

        self.assertEqual(registrations[0].total_time, 150)
        self.assertEqual(registrations[1].total_time, 60)

    def test_registration_get_data(self):
        # Проверка получения записи из бд
        registration = CarWashRegistration.objects.filter(client=self.user1)[0]
        self.assertEqual(str(registration.client), 'Иванов Пётр Николаевич')
        self.assertEqual(str(registration),
                         f'Клиент: {registration.client.fio}, {registration.client.email}')
        self.assertEqual(list(map(str, registration.services.all())), ['Мойка (верх, ковры, сушка)', 'Пылесос салона'])
        self.assertEqual(registration.total_time, 90)

    def test_registration_str(self):
        # Проверка метода __str__()
        expected_str = f'Клиент: {self.registration1.client.fio}, {self.registration1.client.email}'

        self.assertEqual(str(self.registration1), expected_str)


class CarWashWorkDayModelTestCase(TestCase):
    """Тест модели CarWashWorkDay"""

    fixtures = {'services.json'}
    FORMATTED_KEY = ['date', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                     '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00',
                     '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']

    def setUp(self):
        self.services = CarWashService.objects.all()

        self.user1 = User.objects.create(
            email='testuser@mail.ru',
            password='12345qwerty',
            fio='Иванов Пётр Николаевич',
            phone_number='81234567890',
            car_model='Kia Sportage',
        )
        self.user2 = User.objects.create(email='testuser1@mail.ru', password='12345qwerty')

        self.registration1 = CarWashRegistration.objects.create(
            client=self.user1,
            date_reg=date.today(),
            time_reg=time(10, 00),
        )
        self.registration1.services.set([self.services[0], self.services[6]])
        calculate_total_time_and_total_cost(self.registration1)

        self.registration2 = CarWashRegistration.objects.create(
            client=self.user2,
            date_reg=date.today(),
            time_reg=time(13, 00),
        )
        self.registration2.services.set([self.services[1], self.services[2], self.services[3]])
        calculate_total_time_and_total_cost(self.registration2)

        self.workday1 = CarWashWorkDay.objects.create(date=date.today())
        self.workday2 = CarWashWorkDay.objects.create(date=date.today() + timedelta(days=1))
        self.workday2.time_1000 = self.registration1.get_data()
        self.workday2.time_1300 = self.registration2.get_data()

    def test_workday_get_all_records(self):
        # Проверка количества созданных объектов модели WorkDay в бд
        self.assertEqual(CarWashWorkDay.objects.all().count(), 2)

    def test_workday_str(self):
        # Проверка метода __str__()
        expected_str1 = str(date.today())
        expected_str2 = str(date.today() + timedelta(days=1))

        self.assertEqual(str(self.workday1), expected_str1)
        self.assertEqual(str(self.workday2), expected_str2)

    def test_workday_get_formatted_dict(self):
        # Проверка корректной работы метода модели WorkDay: formatted_dict
        workday_values = list(self.workday2.__dict__.values())[2:]
        res_dict = dict((workday_time, value) for workday_time, value in zip(self.FORMATTED_KEY, workday_values))
        res_dict['10:00'] = self.registration1.get_data()
        res_dict['13:00'] = self.registration2.get_data()

        self.assertEqual(self.workday2.formatted_dict(), res_dict)


class CarWashRequestCallModelTestCase(TestCase):
    """Тест модели CarWashRequestCall"""

    def setUp(self):
        self.request_call = CarWashRequestCall.objects.create(phone_number='89999999999')
        CarWashRequestCall.objects.create(phone_number='81111111111')
        CarWashRequestCall.objects.create(phone_number='82222222222')

    def test_fields(self):
        # Проверка полей
        filed_label = self.request_call._meta.get_field('phone_number').verbose_name
        max_length = self.request_call._meta.get_field('phone_number').max_length

        self.assertEqual(filed_label, 'номер телефона')
        self.assertEqual(max_length, 11)

    def test_request_call_get_all_records(self):
        # Проверка количества созданных объектов модели CarWashRequestCall в бд
        self.assertEqual(CarWashRequestCall.objects.all().count(), 3)
