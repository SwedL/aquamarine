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
        self.user.is_admin = True
        self.user.is_superuser = True
        self.permission = Permission.objects.get(codename='view_workday')
        self.all_permission = Permission.objects.all()

    def test_view(self):
        # Проверка
        path = reverse('carwash:home')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Aquamarine')
        self.assertTemplateUsed(response, 'carwash/index.html')
        self.assertEqual(list(response.context_data['object_list']), list(self.services))
        self.assertEqual(self._common_tests(), [])

    def test_if_logged_but_cannot_permission(self):
        self.client.force_login(self.user)
        self.assertEqual(self._common_tests(), ['Профиль', 'Мои записи', 'Выйти'])

    def test_if_logged_and_can_permission(self):
        self.client.force_login(self.user)
        self.user.user_permissions.add(self.permission)

        self.assertEqual(self._common_tests(), ['Профиль', 'Мои записи', 'Сотрудник', 'Выйти'])

    def test_if_logged_and_can_permission_is_admin(self):
        self.user.user_permissions.set(self.all_permission)
        self.user.is_admin = True
        self.user.is_superuser = True
        # self.user.is_staff

        self.client.force_login(self.user)
        result = self._common_tests()
        print(result)
        self.assertEqual(result, ['Профиль', 'Мои записи', 'Сотрудник', 'Выйти'])

    def _common_tests(self):
        path = reverse('carwash:home')
        response = self.client.get(path)

        soup = BeautifulSoup(response.content, 'html.parser')
        result = [r.text for r in soup.find_all('a', class_='dropdown-item')]
        return result


class RegistrationAutoViewTestCase(TestCase):
    fixtures = {'services.json'}

    def setUp(self):
        self.services = dict([(k, v) for k, v in enumerate(CarWashService.objects.all(), start=1)])

    def test_view(self):
        path = reverse('carwash:registration')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'Запись автомобиля')
        self.assertTemplateUsed(response, 'carwash/registration.html')
        self.assertEqual(list(response.context['services']), list(self.services))

    # def test_display


class StaffDetailViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru', password='test')
        self.permission = Permission.objects.get(codename='view_workday')
        self.path = reverse('carwash:staff', kwargs={'days_delta': 0})

    def test_user_cannot_permission(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_user_can_permission(self):
        self.user.user_permissions.add(self.permission)
        self.client.force_login(self.user)
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'Сотрудник')
        self.assertTemplateUsed(response, 'carwash/staff.html')
