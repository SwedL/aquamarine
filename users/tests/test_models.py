from django.test import TestCase

from users.models import User


class UserModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@mail.ru', password='12345qwerty', fio='Иванов Пётр Николаевич',
                                        phone_number='+79445555555', car_model='Kia Sportage')
        User.objects.create(email='testuser2@mail.ru', password='12345qwerty')
        User.objects.create(email='testuser3@mail.ru', password='12345qwerty')
        User.objects.create(email='testuser4@mail.ru', password='12345qwerty')

    def test_user_creation(self):
        # Проверка создания объекта User
        self.assertEqual(self.user.email, 'testuser@mail.ru')
        self.assertEqual(self.user.fio, 'Иванов Пётр Николаевич')
        self.assertEqual(self.user.phone_number, '+79445555555')
        self.assertEqual(self.user.car_type, 'price_standart')
        self.assertEqual(self.user.car_model, 'Kia Sportage')
        self.assertEqual(self.user.discount, 0)

    def test_user_get_all_records(self):
        # Проверка получения всех записей из бд
        users = User.objects.all()
        self.assertEqual(len(users), 4)

    def test_user_get_record(self):
        # Проверка получения записи из бд
        user = User.objects.get(email='testuser@mail.ru')
        self.assertEqual(user.car_type, 'price_standart')
        self.assertEqual(user.discount, 0)

    def test_user_str(self):
        # Проверка метода __str__()
        expected_str = 'testuser@mail.ru'
        self.assertEqual(str(self.user), expected_str)

    def test_user_default_value(self):
        # Проверка значения по умолчанию для объекта User
        user = User.objects.get(email='testuser2@mail.ru')
        self.assertEqual(user.fio, '')
        self.assertEqual(user.phone_number, '')
        self.assertEqual(user.car_type, 'price_standart')
        self.assertEqual(user.car_model, '')
        self.assertEqual(user.discount, 0)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, False)