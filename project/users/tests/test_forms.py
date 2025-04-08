from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from users.forms import (MyPasswordChangeForm, UserForgotPasswordForm,
                           UserLoginForm, UserProfileForm,
                           UserSetNewPasswordForm)
from users.models import User


class UserLoginFormTestCase(TestCase):
    """Тест формы авторизации пользователя"""

    def test_form_field_label(self):
        # Проверка названий полей формы
        form = UserLoginForm()
        self.assertTrue(
            form.fields['username'].label is None or form.fields['username'].label == 'Логин')
        self.assertTrue(
            form.fields['password'].label is None or form.fields['password'].label == 'Пароль')


class UserProfileFormTestCase(TestCase):
    """Тест формы профиля пользователя для изменения данных"""

    def test_form_field_label(self):
        # Проверка названий полей формы
        form = UserProfileForm()

        self.assertTrue(
            form.fields['email'].label is None or form.fields['email'].label == 'Логин')
        self.assertTrue(
            form.fields['fio'].label is None or form.fields['fio'].label == 'ФИО')
        self.assertTrue(
            form.fields['phone_number'].label is None or form.fields['phone_number'].label == 'номер телефона')
        self.assertTrue(
            form.fields['car_model'].label is None or form.fields['car_model'].label == 'Марка и модель автомобиля')

    def test_form_is_valid_value(self):
        # Проверка на валидность вводимых значений в форму
        form_data = {
            'email': 'test@mail.ru',
            'fio': 'Иванов Петр Николаевич',
            'phone_number': '81234567890',
            'car_model': 'Kia Sportage',
            }
        form = UserProfileForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_is_not_valid_email_value(self):
        # Проверка на не валидность значения email
        form_data = {
            'email': 'test.ru',
            'fio': 'Иванов Петр Николаевич',
            'phone_number': '81234567890',
            'car_model': 'Kia Sportage',
        }
        form = UserProfileForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_phone_number_value(self):
        # Проверка на не валидность значения phone_number
        form_data = {
            'email': 'test@mail.ru',
            'fio': 'Иванов Петр Николаевич',
            'phone_number': '91234567890',
            'car_model': 'Kia Sportage',
            }
        form = UserProfileForm(data=form_data)

        self.assertFalse(form.is_valid())


class MyPasswordChangeFormTestCase(TestCase):
    """Тест формы смены пароля пользователя"""

    def setUp(self):
        self.user1 = User.objects.create(email='testuser@mail.ru', password='12345qwerty')

    def test_form_field_label(self):
        # Проверка названий полей формы
        self.form = MyPasswordChangeForm(self.user1)

        self.assertTrue(
            self.form.fields['old_password'].label is None or
            self.form.fields['old_password'].label == _("Old password")
        )
        self.assertTrue(
            self.form.fields['new_password1'].label is None or
            self.form.fields['new_password1'].label == _('New password')
        )
        self.assertTrue(
            self.form.fields['new_password2'].label is None or
            self.form.fields['new_password2'].label == _('New password confirmation')
        )


class UserForgotPasswordFormTestCase(TestCase):
    """Тест формы запроса на восстановление пароля"""

    def test_form_field_label(self):
        # Проверка поля формы на max_length
        form = UserForgotPasswordForm()

        self.assertEqual(form.fields['email'].max_length, 254)

    def test_form_is_valid_value(self):
        # Проверка на валидность вводимого значения в форму
        form_data = {'email': 'test@mail.ru'}
        form = UserForgotPasswordForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_is_not_valid_value(self):
        # Проверка на не валидность вводимого значения в форму
        form_data = {'email': 'test.ru'}
        form = UserForgotPasswordForm(data=form_data)

        self.assertFalse(form.is_valid())


class UserSetNewPasswordFormTestCase(TestCase):
    """Тест формы для установки нового пароля пользователя по ссылке на эл.почте"""

    def setUp(self):
        self.user1 = User.objects.create(email='testuser@mail.ru', password='12345qwerty')

    def test_form_field_label(self):
        # Проверка названий полей формы
        form = UserSetNewPasswordForm(self.user1)

        self.assertTrue(
            form.fields['new_password1'].label is None or
            form.fields['new_password1'].label == _('New password')
        )
        self.assertTrue(
            form.fields['new_password2'].label is None or
            form.fields['new_password2'].label == _('New password confirmation')
        )

    def test_form_is_valid_value(self):
        # Проверка на валидность вводимых значений в форму
        form_data = {
            'new_password1': '123k10-2t',
            'new_password2': '123k10-2t',
        }
        form = UserSetNewPasswordForm(self.user1, data=form_data)

        self.assertTrue(form.is_valid())
