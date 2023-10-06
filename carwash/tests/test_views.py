from http import HTTPStatus

from bs4 import BeautifulSoup
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from carwash.models import CarWashService
from users.models import User


class IndexListViewTestCase(TestCase):
    fixtures = {'services.json'}

    def setUp(self):
        self.services = CarWashService.objects.all()
        self.user = User.objects.create(email='test@mail.ru', password='test')
        self.permission = Permission.objects.get(codename='view_workday')
        self.path = reverse('carwash:home')

    def test_view(self):
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

    def test_display_submit_button_if_unregistered_user(self):
        # Проверка отображения кнопки формы для неавторизованного пользователя
        self.assertEqual(self._common_tests('call-me__button'), 'Заказать звонок')

    def test_display_submit_button_if_logged_user(self):
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
