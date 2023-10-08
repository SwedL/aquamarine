from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserLoginViewTestCase(TestCase):

    def test_view(self):
        # Проверка представления страницы авторизации пользователя
        path = reverse('users:login')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Авторизация')
        self.assertTemplateUsed(response, 'users/login.html')


class UserProfileViewTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(email='testuser@mail.ru', password='12345qwerty', fio='Иванов Пётр Николаевич',
                                         phone_number='+79445555555', car_model='Kia Sportage')

    def test_view(self):
        # Проверка представления страницы профиля пользователя
        path = reverse('users:profile')
        self.client.force_login(self.user1)
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Настройка профиля')
        self.assertTemplateUsed(response, 'users/profile.html')


class UserPasswordChangeViewTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(email='testuser@mail.ru', password='12345qwerty', fio='Иванов Пётр Николаевич',
                                         phone_number='+79445555555', car_model='Kia Sportage')

    def test_view(self):
        # Проверка представления страницы смены пароля пользователем
        path = reverse('users:password_change')
        self.client.force_login(self.user1)
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Смена пароля')
        self.assertTemplateUsed(response, 'users/password-change.html')


class UserForgotPasswordViewTestCase(TestCase):

    def test_view(self):
        # Проверка представления страницы для сброса пароля пользователем
        path = reverse('users:password_reset')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Запрос на сброс пароля')
        self.assertTemplateUsed(response, 'users/user-password-reset.html')


class PasswordChangeDoneTemplateViewTestCase(TestCase):

    def test_view(self):
        # Проверка представления для подтверждения успешной смены пароля пользователем
        path = reverse('users:password_change_done')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Aquamarine')
        self.assertTemplateUsed(response, 'users/password-change-done.html')

