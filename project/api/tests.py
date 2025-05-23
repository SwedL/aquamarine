from collections import OrderedDict
from datetime import date

from carwash.models import CarWashRegistration, CarWashService, CarWashWorkDay
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.models import User


class CarWashServiceListAPIViewTests(APITestCase):
    """Тест на получение полного списка услуг автомоечного комплекса"""

    fixtures = {'services.json'}

    def test_get_all_services(self):
        url = reverse('api:service_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CarWashService.objects.count(), 17)
        self.assertEqual(CarWashService.objects.first().name, 'Мойка (верх, ковры, сушка)')


class CarWashRegistrationAPIViewTestCase(APITestCase):
    """Тест представления записи автомобиля на автомоечный комплекс"""

    fixtures = {'services.json'}

    def setUp(self):
        self.user = User.objects.create(
            email='testuser@mail.ru',
            password='12345qwerty',
        )
        self.workday = CarWashWorkDay.objects.create(date=date.today())
        self.url = reverse('api:carwash_registration')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CarWashService.objects.count(), 17)
        self.assertEqual(CarWashWorkDay.objects.count(), 7)

    def test_registration_auto_at_carwash(self):
        selected_date = str(date.today()).replace('-', ' ')
        selected_time = '10:00'
        data = {'selected_date_and_time': f'{selected_date},{selected_time}', 'services_ids': '15'}

        response = self.client.post(self.url, data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['title'], 'Запись зарегистрирована')
        self.assertEqual(response_json['selected_services'],
                         [{
                             'id': 15,
                             'name': 'Удаление стойких загрязнений с кузова',
                             'process_time': 60,
                             'price_standart': 450,
                             'price_crossover': 500,
                             'price_offroad': 500,
                         }]
                         )
        self.assertEqual(response_json['selected_date'], selected_date)
        self.assertEqual(response_json['selected_time'], selected_time)
        self.assertEqual(response_json['total_time'], 60)
        self.assertEqual(response_json['total_cost'], '450 р.')

    def test_post_data_then_selected_time_is_already_taken(self):
        choice_date = str(date.today()).replace('-', ' ')
        data = {'selected_date_and_time': f'{choice_date},10:00', 'services_ids': '15'}
        self.client.post(self.url, data, format='json')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data, {
            "title": "Ошибка записи",
            "message": "Время которые вы выбрали уже занято. Попробуйте выбрать другое время"
        })


class CarWashUserRegistrationAPIViewTestCase(APITestCase):
    """
    Тестирование представления получения списка записей пользователя
    на автомоечный комплекс и возможность их отмены (удаления) пользователем
    """

    fixtures = {'services.json'}

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email='testuser@mail.ru',
            password='12345qwerty',
        )

    def setUp(self):
        """
        Создаём пользователя, создаём 2 записи автомобиля на автомоечный комплекс,
        автоматически создаются 2 записи в личном кабинете пользователя,
        которые пользователь может просматривать и удалять
        """

        self.url = reverse('api:user_registration_list')
        self.workday = CarWashWorkDay.objects.create(date=date.today())
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_user_registration_list(self):
        # проверяем получения информации о записях автомобиля пользователя CarWashUserRegistration
        choice_date = str(date.today()).replace('-', ' ')
        data1 = {'selected_date_and_time': f'{choice_date},10:00', 'services_ids': '1'}
        data2 = {'selected_date_and_time': f'{choice_date},14:00', 'services_ids': '3'}
        self.client.post(reverse('api:carwash_registration'), data1, format='json')
        self.client.post(reverse('api:carwash_registration'), data2, format='json')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(CarWashRegistration.objects.all()), 2)
        self.assertEqual(response.data, [
            OrderedDict([
                ('id', 6),
                ('client', self.user.id),
                ('services', ['Мойка (верх, ковры, сушка)']),
                ('date_reg', str(date.today())),
                ('time_reg', '10:00:00'),
                ('total_time', 60),
                ('total_cost', 450),
                ('relation_carwashworkday', {'time_attributes': ['time_1000', 'time_1030']})
            ]),
            OrderedDict([
                ('id', 7),
                ('client', self.user.id),
                ('services', ['Экспресс-мойка']),
                ('date_reg', str(date.today())),
                ('time_reg', '14:00:00'),
                ('total_time', 30),
                ('total_cost', 200),
                ('relation_carwashworkday', {'time_attributes': ['time_1400']})
            ])
        ])

    def test_delete_user_registration(self):
        # проверяем возможность удаления записи автомобиля пользователя CarWashUserRegistration
        choice_date = str(date.today()).replace('-', ' ')
        data1 = {'selected_date_and_time': f'{choice_date},10:00', 'services_ids': '1'}
        data2 = {'selected_date_and_time': f'{choice_date},14:00', 'services_ids': '3'}
        self.client.post(reverse('api:carwash_registration'), data1, format='json')
        self.client.post(reverse('api:carwash_registration'), data2, format='json')
        user_registration_all = CarWashRegistration.objects.all()
        need_id = user_registration_all.first().id
        self.assertEqual(len(user_registration_all), 2)
        new_reverse = reverse('api:user_registration_delete', kwargs={'pk': need_id})
        self.client.delete(new_reverse)
        self.assertEqual(len(CarWashRegistration.objects.all()), 1)


class CarWashRequestCallCreateAPIViewTestCase(APITestCase):
    """Тест представления заказа звонка авторизованного пользователя"""

    def setUp(self):
        self.user = User.objects.create(
            email='testuser@mail.ru',
            password='12345qwerty',
        )
        self.url = reverse('api:carwash_request_call')

    def test_creating_call_request_unauthorized_user(self):
        data = {'phone_number': '89111111111'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_call_request_authorized_user(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        data = {'phone_number': '89111111111'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creating_call_request_authorized_user_not_valid_data(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        data = {'phone_number': '89111111'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'phone_number': ['Номер телефона должен быть в формате: "89999999999"']})


class UserProfileDetailAPIViewTestCase(APITestCase):
    """Тестирование представления получения данных профиля пользователя и их изменение"""

    def setUp(self):
        self.user = User.objects.create(
            email='testuser@mail.ru',
            password='12345qwerty',
            fio='Иванов Пётр Николаевич',
            phone_number='89445555555',
            car_model='Kia Sportage',
        )
        self.url = reverse('api:user_profile')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_data_user_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'email': 'testuser@mail.ru',
                                         'fio': 'Иванов Пётр Николаевич',
                                         'phone_number': '89445555555',
                                         'car_type': 'price_standart',
                                         'car_model': 'Kia Sportage',
                                         })

    def test_change_data_user_profile(self):
        """
        изменяются данные в полях ('fio', 'phone_number, 'car_model'),
        остальные поля только для чтения ('email', 'car_type', 'discount')
        """
        data = {'email': 'newtestuser@mail.ru',
                'fio': 'Петров Николай Иванович',
                'phone_number': '89443333333',
                'car_type': 'price_s',
                'car_model': 'Kia Venga', }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'email': 'testuser@mail.ru',
                                         'fio': 'Петров Николай Иванович',
                                         'phone_number': '89443333333',
                                         'car_type': 'price_standart',
                                         'car_model': 'Kia Venga',
                                         })
