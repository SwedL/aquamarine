from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from carwash.models import *
from users.models import User


class CarWashServiceModelTestCase(TestCase):

    @staticmethod
    def print_info(message):
        count = CarWashService.objects.count()
        print(f"{message}: #all_services={count}")

    def setUp(self):
        print('-' * 20)
        self.print_info('Start setUp')
        self.service = CarWashService.objects.create(name='Мойка (верх, ковры, сушка)', process_time=60,
                                                     price_standart=450, price_crossover=550, price_offroad=650)
        CarWashService.objects.create(name='Экспресс-мойка', process_time=30, price_standart=200, price_crossover=200,
                                      price_offroad=250)
        CarWashService.objects.create(name='Экспресс-мойка с шампунем', process_time=30, price_standart=250,
                                      price_crossover=250, price_offroad=300)
        self.print_info('Finish setUp')

    def test_service_creation(self):
        # Проверка создания объекта CarWashService
        self.print_info('Start test_service_creation')
        self.assertEqual(self.service.name, 'Мойка (верх, ковры, сушка)')
        self.assertEqual(self.service.process_time, 60)
        self.assertEqual(self.service.price_standart, 450)
        self.assertEqual(self.service.price_crossover, 550)
        self.assertEqual(self.service.price_offroad, 650)
        self.print_info('Finish test_service_creation')

    def test_service_get_all_records(self):
        # Проверка получения всех записей из бд
        self.print_info('Start test_service_get_all_records')
        services = CarWashService.objects.all()
        self.assertEqual(len(services), 3)
        self.print_info('Finish test_service_get_all_records')

    def test_service_get_record(self):
        # Проверка получения записи из бд
        self.print_info('Start test_service_get_record')
        carwash = CarWashService.objects.get(name='Мойка (верх, ковры, сушка)')
        self.assertEqual(carwash.process_time, 60)
        self.print_info('Finish test_service_get_record')

    def test_service_str(self):
        # Проверка метода __str__()
        self.print_info('Start test_service_str')
        expected_str = 'Мойка (верх, ковры, сушка)'
        self.assertEqual(str(self.service), expected_str)
        self.print_info('Finish test_service_str')

    def test_service_process_time_and_price_default_value(self):
        # Проверка значений по умолчанию объекта CarWashService
        self.print_info('Start test_service_process_time_and_price_default_value')
        service = CarWashService.objects.create(name='Default Price Service')
        self.assertEqual(service.process_time, 0)
        self.assertEqual(service.price_standart, 0)
        self.assertEqual(service.price_crossover, 0)
        self.assertEqual(service.price_offroad, 0)
        self.print_info('Finish test_service_process_time_and_price_default_value')


class UserModelTestCase(TestCase):
    @staticmethod
    def print_info(message):
        count = User.objects.count()
        print(f"{message}: #all_users={count}")

    def setUp(self):
        print('-' * 20)
        self.print_info('Start setUp')
        self.user = User.objects.create(email='testuser@mail.ru', password='12345qwerty', fio='Иванов Пётр Николаевич',
                                        tel='+79445555555', car_model='Kia Sportage')
        User.objects.create(email='testuser2@mail.ru', password='12345qwerty')
        User.objects.create(email='testuser3@mail.ru', password='12345qwerty')
        User.objects.create(email='testuser4@mail.ru', password='12345qwerty')
        self.print_info('Finish setUp')

    def test_user_creation(self):
        # Проверка создания объекта User
        self.print_info('Start test_user_creation')
        self.assertEqual(self.user.email, 'testuser@mail.ru')
        self.assertEqual(self.user.fio, 'Иванов Пётр Николаевич')
        self.assertEqual(self.user.tel, '+79445555555')
        self.assertEqual(self.user.car_type, 'price_standart')
        self.assertEqual(self.user.car_model, 'Kia Sportage')
        self.assertEqual(self.user.discount, 0)
        self.print_info('Finish test_user_creation')

    def test_user_get_all_records(self):
        # Проверка получения всех записей из бд
        self.print_info('Start test_user_get_all_records')
        users = User.objects.all()
        self.assertEqual(len(users), 4)
        self.print_info('Finish test_user_get_all_records')

    def test_user_get_record(self):
        # Проверка получения записи из бд
        self.print_info('Start test_user_get_record')
        user = User.objects.get(email='testuser@mail.ru')
        self.assertEqual(user.car_type, 'price_standart')
        self.assertEqual(user.discount, 0)
        self.print_info('Finish test_user_get_record')

    def test_user_str(self):
        # Проверка метода __str__()
        self.print_info('Start test_user_str')
        expected_str = 'testuser@mail.ru'
        self.assertEqual(str(self.user), expected_str)
        self.print_info('Finish test_user_str')

    def test_user_default_value(self):
        # Проверка значения по умолчанию для объекта User
        self.print_info('Start test_user_default_value')
        user = User.objects.get(email='testuser2@mail.ru')
        self.assertEqual(user.fio, '')
        self.assertEqual(user.tel, '')
        self.assertEqual(user.car_type, 'price_standart')
        self.assertEqual(user.car_model, '')
        self.assertEqual(user.discount, 0)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, False)
        self.print_info('Finish test_user_default_value')


class CarWashRegistrationModel(TestCase):
    @staticmethod
    def print_info(message):
        count = CarWashRegistration.objects.count()
        print(f"{message}: #all_registrations={count}")

    def setUp(self):
        print('-' * 20)
        self.print_info('Start setUp')
        self.user1 = User.objects.create(email='testuser@mail.ru', password='12345qwerty', fio='Иванов Пётр Николаевич',
                                        tel='+79445555555', car_model='Kia Sportage')
        self.user2 = User.objects.create(email='testuser1@mail.ru', password='12345qwerty')
        self.service1 = CarWashService.objects.create(name='Мойка (верх, ковры, сушка)', process_time=60,
                                                      price_standart=450, price_crossover=550, price_offroad=650)
        self.service2 = CarWashService.objects.create(name='Пылесос салона', process_time=30, price_standart=100,
                                                      price_crossover=100,
                                                      price_offroad=150)
        self.service3 = CarWashService.objects.create(name='Экспресс-мойка с шампунем', process_time=30,
                                                      price_standart=250,
                                                      price_crossover=250, price_offroad=300)
        self.service4 = CarWashService.objects.create(name='Экспресс-мойка2', process_time=30)
        self.service5 = CarWashService.objects.create(name='Экспресс-мойка3', process_time=30),
        self.service6 = CarWashService.objects.create(name='Экспресс-мойка4', process_time=30)
        self.service7 = CarWashService.objects.create(name='Экспресс-мойка7', process_time=30)
        self.service8 = CarWashService.objects.create(name='Экспресс-мойка8', process_time=30)
        self.service9 = CarWashService.objects.create(name='Экспресс-мойка9', process_time=30)

        self.registration1 = CarWashRegistration.objects.create(client=self.user1)
        [self.registration1.services.add(s) for s in (self.service1, self.service2)]

        self.registration2 = CarWashRegistration.objects.create(client=self.user1)
        [self.registration2.services.add(s) for s in (self.service3, self.service2)]

        self.registration3 = CarWashRegistration.objects.create(client=self.user2)
        self.registration3.services.add(self.service1, self.service2, self.service3)

        self.registration789 = CarWashRegistration.objects.create(client=self.user2)
        [self.registration789.services.add(s) for s in (self.service1, self.service7, self.service8, self.service9)]
        self.print_info('Finish setUp')

    def test_registration_creation(self):
        # Проверка создания объекта CarWashRegistration
        self.print_info('Start test_registration_creation')
        self.assertEqual(str(self.registration1.client), 'testuser@mail.ru')
        self.assertEqual(str(self.registration1), 'testuser@mail.ru || Kia Sportage || Мойка (верх, ковры, сушка), Пылесос салона')
        self.print_info('Finish test_registration_creation')

    def test_registration_get_all_records(self):
        # Проверка получения всех записей из бд
        self.print_info('Start test_registration_get_all_records')
        registrations = CarWashRegistration.objects.all()
        self.assertEqual(len(registrations), 4)
        self.print_info('Finish test_registration_get_all_records')

    def test_registration_get_total_time(self):
        self.print_info('Start test_registration_get_total_time')
        registrations = CarWashRegistration.objects.filter(client=self.user2)
        self.assertEqual(registrations[0].total_time, 120)
        self.assertEqual(registrations[1].total_time, 90)
        self.print_info('Finish test_registration_get_total_time')

    def test_registration_get_record(self):
        # Проверка получения записи из бд
        self.print_info('Start test_registration_get_record')
        registration = CarWashRegistration.objects.filter(client=self.user1)[0]
        self.assertEqual(str(registration.client), 'testuser@mail.ru')
        self.assertEqual(list(map(str, registration.services.all())), ['Мойка (верх, ковры, сушка)', 'Пылесос салона'])
        self.assertEqual(registration.total_time, 90)
        self.print_info('Finish test_registration_get_record')

    def test_registration_str(self):
        # Проверка метода __str__()
        self.print_info('Start test_registration_str')
        expected_str = 'testuser@mail.ru || Kia Sportage || Мойка (верх, ковры, сушка), Пылесос салона'
        self.assertEqual(str(self.registration1), expected_str)
        self.print_info('Finish test_registration_str')

    # def test_user_default_value(self):
    #     # Проверка значения по умолчанию для budget
    #     self.print_info('Start test_user_default_value')
    #     user = User.objects.get(email='testuser2@mail.ru')
    #     self.assertEqual(user.fio, '')
    #     self.assertEqual(user.tel, '')
    #     self.assertEqual(user.car_type, 'price_standart')
    #     self.assertEqual(user.car_model, '')
    #     self.assertEqual(user.discount, 0)
    #     self.assertEqual(user.is_active, True)
    #     self.assertEqual(user.is_admin, False)
    #     self.print_info('Finish test_user_default_value')


class IndexListViewTestCase(TestCase):
    def test_view(self):
        path = ''
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Aquamarine')
        self.assertTemplateUsed(response, 'carwash/index.html')
