from django.test import TestCase

from carwash.models import *


class CarWashServiceModelTestCase(TestCase):
    def setUp(self):
        self.service = CarWashService.objects.create(name='Мойка (верх, ковры, сушка)', process_time=60,
                                                     price_standart=450, price_crossover=550, price_offroad=650)
        CarWashService.objects.create(name='Экспресс-мойка', process_time=30, price_standart=200, price_crossover=200,
                                      price_offroad=250)
        CarWashService.objects.create(name='Экспресс-мойка с шампунем', process_time=30, price_standart=250,
                                      price_crossover=250, price_offroad=300)

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
        services = CarWashService.objects.all()
        self.assertEqual(len(services), 3)

    def test_service_get_record(self):
        # Проверка получения записи из бд
        carwash = CarWashService.objects.get(name='Мойка (верх, ковры, сушка)')
        self.assertEqual(carwash.process_time, 60)

    def test_service_str(self):
        # Проверка метода __str__()
        expected_str = 'Мойка (верх, ковры, сушка)'
        self.assertEqual(str(self.service), expected_str)

    def test_service_process_time_and_price_default_value(self):
        # Проверка значений по умолчанию объекта CarWashService
        service = CarWashService.objects.create(name='Default Price Service')
        self.assertEqual(service.process_time, 0)
        self.assertEqual(service.price_standart, 0)
        self.assertEqual(service.price_crossover, 0)
        self.assertEqual(service.price_offroad, 0)


class CarWashRegistrationModelTestCase(TestCase):
    fixtures = {'services.json'}

    def setUp(self):
        self.user1 = User.objects.create(email='testuser@mail.ru', password='12345qwerty', fio='Иванов Пётр Николаевич',
                                         phone_number='+79445555555', car_model='Kia Sportage')
        self.user2 = User.objects.create(email='testuser1@mail.ru', password='12345qwerty')

        self.services = CarWashService.objects.all()

        self.registration1 = CarWashRegistration.objects.create(client=self.user1)
        self.registration1.services.set([self.services[0], self.services[6]])

        self.registration2 = CarWashRegistration.objects.create(client=self.user2)
        self.registration2.services.set([self.services[1], self.services[2], self.services[3]])

        self.registration789 = CarWashRegistration.objects.create(client=self.user2)
        self.registration789.services.set([self.services[3], self.services[6], self.services[7], self.services[8]])

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

    def test_registration_creation(self):
        # Проверка создания объекта CarWashRegistration
        self.assertEqual(str(self.registration1.client), 'testuser@mail.ru')
        self.assertEqual(str(self.registration1),
                         'testuser@mail.ru || Kia Sportage || Мойка (верх, ковры, сушка), Пылесос салона')

    def test_registration_get_all_records(self):
        # Проверка количества созданных объектов модели CarWashRegistration в бд
        registrations = CarWashRegistration.objects.all()
        self.assertEqual(len(registrations), 3)

    def test_registration_get_total_time(self):
        # Проверка правильного подсчёта полного времени выбранных услуг Записи (услуги 7,8,9 считаются как за одну)
        registrations = CarWashRegistration.objects.filter(client=self.user2)
        self.assertEqual(registrations[0].total_time, 150)
        self.assertEqual(registrations[1].total_time, 60)

    def test_registration_get_record(self):
        # Проверка получения записи из бд
        registration = CarWashRegistration.objects.filter(client=self.user1)[0]
        self.assertEqual(str(registration.client), 'testuser@mail.ru')
        self.assertEqual(list(map(str, registration.services.all())), ['Мойка (верх, ковры, сушка)', 'Пылесос салона'])
        self.assertEqual(registration.total_time, 90)

    def test_registration_str(self):
        # Проверка метода __str__()
        expected_str = 'testuser@mail.ru || Kia Sportage || Мойка (верх, ковры, сушка), Пылесос салона'
        self.assertEqual(str(self.registration1), expected_str)


class WorkDayModelTestCase(TestCase):
    fixtures = {'services.json'}
    FORMATTED_KEY = ['date', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                     '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00',
                     '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30'
                     ]

    def setUp(self):
        self.services = CarWashService.objects.all()

        self.user1 = User.objects.create(email='testuser@mail.ru', password='12345qwerty', fio='Иванов Пётр Николаевич',
                                         phone_number='+79445555555', car_model='Kia Sportage')
        self.user2 = User.objects.create(email='testuser1@mail.ru', password='12345qwerty')

        self.registration1 = CarWashRegistration.objects.create(client=self.user1)
        self.registration1.services.set([self.services[0], self.services[1]])

        self.registration2 = CarWashRegistration.objects.create(client=self.user2)
        self.registration2.services.set([self.services[2], self.services[1]])

        self.workday1 = WorkDay.objects.create(date=date.today())

        self.workday2 = WorkDay.objects.create(date=date.today() + timedelta(days=1))
        self.workday2.time_1000 = self.registration1
        self.workday2.time_1300 = self.registration2

    def test_workday_creation(self):
        # Проверка создания объекта WorkDay
        self.assertEqual(self.workday1.date, date.today())
        self.assertEqual(self.workday2.time_1000, self.registration1)
        self.assertEqual(self.workday2.time_1300, self.registration2)

    def test_workday_get_all_records(self):
        # Проверка количества созданных объектов модели WorkDay в бд
        workdays = WorkDay.objects.all()
        self.assertEqual(len(workdays), 2)

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
        res_dict['10:00'] = self.registration1.pk
        res_dict['13:00'] = self.registration2.pk
        self.assertEqual(self.workday2.formatted_dict(), res_dict)


class CarWashUserRegistrationModelTestCase(TestCase):
    fixtures = {'services.json'}

    def setUp(self):
        self.services = CarWashService.objects.all()

        self.user1 = User.objects.create(email='testuser@mail.ru', password='12345qwerty', fio='Иванов Пётр Николаевич',
                                         phone_number='+79445555555', car_model='Kia Sportage')
        self.user2 = User.objects.create(email='testuser1@mail.ru', password='12345qwerty')

        self.registration1 = CarWashRegistration.objects.create(client=self.user1)
        self.registration1.services.set([self.services[0], self.services[6]])

        self.registration2 = CarWashRegistration.objects.create(client=self.user2)
        self.registration2.services.set([self.services[1], self.services[2], self.services[3]])

        CarWashUserRegistration.objects.create(
            client=self.user1,
            date_reg=date(2023, 10, 7),
            time_reg=time(12, 00),
            carwash_reg=self.registration1,
        )

        CarWashUserRegistration.objects.create(
            client=self.user2,
            date_reg=date(2023, 10, 7),
            time_reg=time(10, 00),
            carwash_reg=self.registration2,
        )

    def test_fields(self):
        # Проверка полей
        user_registrations = CarWashUserRegistration.objects.all().first()
        field_client = user_registrations._meta.get_field('client').verbose_name
        field_date_reg = user_registrations._meta.get_field('date_reg').verbose_name
        field_time_reg = user_registrations._meta.get_field('time_reg').verbose_name
        field_carwash_reg = user_registrations._meta.get_field('carwash_reg')
        self.assertEqual(field_client, 'клиент')
        self.assertEqual(field_date_reg, 'дата записи')
        self.assertEqual(field_time_reg, 'время записи')
        self.assertTrue(field_carwash_reg.many_to_one)
        self.assertIs(field_carwash_reg.model, CarWashUserRegistration)


    def test_registration_get_all_records(self):
        # Проверка количества созданных объектов модели CarWashUserRegistration в бд
        user_registrations = CarWashUserRegistration.objects.all()
        self.assertEqual(len(user_registrations), 2)


class CarWashRequestCallModelTestCase(TestCase):

    def setUp(self):
        self.request_call = CarWashRequestCall.objects.create(phone_number='89999999999')
        CarWashRequestCall.objects.create(phone_number='81111111111')
        CarWashRequestCall.objects.create(phone_number='82222222222')

    def test_fields(self):
        # Проверка полей
        filed_label = self.request_call._meta.get_field('phone_number').verbose_name
        max_length = self.request_call._meta.get_field('phone_number').max_length
        self.assertEquals(filed_label, 'номер телефона')
        self.assertEquals(max_length, 11)

    def test_request_call_get_all_records(self):
        # Проверка количества созданных объектов модели CarWashRequestCall в бд
        requests_calls = CarWashRequestCall.objects.all()
        self.assertEqual(len(requests_calls), 3)

