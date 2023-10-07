from http import HTTPStatus
from bs4 import BeautifulSoup
from datetime import date, time

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from carwash.models import CarWashService, CarWashRegistration, CarWashUserRegistration
from users.models import User


class IndexListViewTestCase(TestCase):
    fixtures = {'services.json'}

    def setUp(self):
        self.services = CarWashService.objects.all()
        self.user = User.objects.create(email='test@mail.ru', password='test')
        self.permission = Permission.objects.get(codename='view_workday')
        self.path = reverse('carwash:home')

    def test_view_for_not_logged_user(self):
        # Проверка представления главной страницы и меню для неавторизованных пользователей
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Aquamarine')
        self.assertTemplateUsed(response, 'carwash/index.html')
        self.assertEqual(list(response.context_data['object_list']), list(self.services))
        self.assertEqual(self._common_tests(), [])

    def test_if_logged_but_cannot_permission(self):
        # Проверка отображения меню для авторизованного пользователя, но без допуска
        self.client.force_login(self.user)

        self.assertEqual(self._common_tests(), ['Профиль', 'Мои записи', 'Выйти'])

    def test_if_logged_and_can_permission(self):
        # Проверка отображения меню для авторизованного пользователя с допуском
        self.user.user_permissions.add(self.permission)
        self.client.force_login(self.user)

        self.assertEqual(self._common_tests(), ['Профиль', 'Мои записи', 'Сотрудник', 'Выйти'])

    def test_if_logged_and_can_permission_and_is_admin(self):
        # Проверка отображения меню для авторизованного пользователя, с допуском администратора
        self.user.user_permissions.add(self.permission)
        self.user.is_admin = True
        self.user.save()
        self.client.force_login(self.user)

        self.assertEqual(self._common_tests(), ['Профиль', 'Мои записи', 'Сотрудник', 'Админ-панель', 'Выйти'])

    def _common_tests(self):
        response = self.client.get(self.path)

        soup = BeautifulSoup(response.content, 'html.parser')
        result = [r.text for r in soup.find_all('a', class_='dropdown-item')]
        return result


class RegistrationAutoViewTestCase(TestCase):
    fixtures = {'services.json'}

    def setUp(self):
        self.services = dict([(k, v) for k, v in enumerate(CarWashService.objects.all(), start=1)])
        self.user = User.objects.create(email='test@mail.ru', password='test')
        self.path = reverse('carwash:registration')

    def test_view(self):
        # Проверка представления страницы записи автомобиля на автомоечный комплекс
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'Запись автомобиля')
        self.assertTemplateUsed(response, 'carwash/registration.html')
        self.assertEqual(list(response.context['services']), list(self.services))

    def test_display_submit_button_for_not_logged_user(self):
        # Проверка отображения кнопки формы для неавторизованного пользователя
        self.assertEqual(self._common_tests('call-me__button'), 'Заказать звонок')

    def test_display_submit_button_for_logged_user(self):
        # Проверка отображения кнопки формы для авторизованного пользователя
        self.client.force_login(self.user)
        self.assertEqual(self._common_tests('registration__button'), 'Записаться')

    def _common_tests(self, sample):
        response = self.client.get(self.path)
        soup = BeautifulSoup(response.content, 'html.parser')

        return soup.find('div', class_=sample).text.strip()


class StaffDetailViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru', password='test')
        self.permission = Permission.objects.get(codename='view_workday')
        self.path = reverse('carwash:staff', kwargs={'days_delta': 0})

    def test_user_cannot_permission(self):
        # Проверка доступа к странице неавторизованного пользователя
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_user_can_permission(self):
        # Проверка доступа к странице авторизованного пользователя
        self.user.user_permissions.add(self.permission)
        self.client.force_login(self.user)
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'Сотрудник')
        self.assertTemplateUsed(response, 'carwash/staff.html')


class UserRegistrationsListViewTestCase(TestCase):
    fixtures = {'services.json'}

    def setUp(self):
        self.path = reverse('carwash:user_registrations')
        self.services = CarWashService.objects.all()

        self.user1 = User.objects.create(email='testuser@mail.ru', password='12345qwerty', fio='Иванов Пётр Николаевич',
                                         phone_number='+79445555555', car_model='Kia Sportage')

        self.registration1 = CarWashRegistration.objects.create(client=self.user1)
        self.registration1.services.set([self.services[0], self.services[6]])

        self.registration2 = CarWashRegistration.objects.create(client=self.user1)
        self.registration2.services.set([self.services[1], self.services[2], self.services[3]])

        CarWashUserRegistration.objects.create(
            client=self.user1,
            date_reg=date(2023, 10, 7),
            time_reg=time(12, 00),
            carwash_reg=self.registration1,
        )

        CarWashUserRegistration.objects.create(
            client=self.user1,
            date_reg=date(2023, 10, 9),
            time_reg=time(10, 00),
            carwash_reg=self.registration2,
        )


class UserRegistrationsCancelViewTestCase(TestCase):
    pass


class RequestCallFormViewTestCase(TestCase):
    pass
