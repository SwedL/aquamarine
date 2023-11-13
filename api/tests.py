# from django.test import TestCase
import json
from datetime import date

from django.urls import reverse
from rest_framework.test import force_authenticate

from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from carwash.models import CarWashService, WorkDay
from users.models import User
from api.views import CarWashRegistrationAPIView


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
        self.workday = WorkDay.objects.create(date=date.today())
        self.url = reverse('api:carwash_registration')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CarWashService.objects.count(), 17)
        self.assertEqual(WorkDay.objects.count(), 7)

    def test_post_data(self):
        current_date = str(date.today()).replace('-', ' ')
        data = {'choice_date_and_time': f'{current_date},10:00',
                'service_1': '1',
                'service_15': '15',
                'service_17': '17',
                }

        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(CarWashService.objects.count(), 17)
        # self.assertEqual(WorkDay.objects.count(), 7)


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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        self.assertEqual(response.data, {'phone_number': ['Номер телефона должен быть в формате: "89999999999"']})


class UserProfileDetailAPIViewTestCase(APITestCase):
    """Тестирование получения данных профиля пользователя и их изменение"""
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
                                         'discount': 0,
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
                'car_model': 'Kia Venga',
                'discount': 50,
                }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'email': 'testuser@mail.ru',
                                         'fio': 'Петров Николай Иванович',
                                         'phone_number': '89443333333',
                                         'car_type': 'price_standart',
                                         'car_model': 'Kia Venga',
                                         'discount': 0,
                                         })
