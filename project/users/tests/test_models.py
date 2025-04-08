from django.test import TestCase

from users.models import User


class UserModelTestCase(TestCase):
    """Тест модели Пользователь"""

    def setUp(self):
        self.user = User.objects.create(
            email='testuser@mail.ru',
            password='12345qwerty',
            fio='Иванов Пётр Николаевич',
            phone_number='89445555555',
            car_model='Kia Sportage',
        )
        User.objects.create(email='testuser2@mail.ru', password='12345qwerty')
        User.objects.create(email='testuser3@mail.ru', password='12345qwerty')
        User.objects.create(email='testuser4@mail.ru', password='12345qwerty')

    def test_fields(self):
        # Проверка полей модели на названия и default значения
        user = User.objects.all().first()
        field_email = user._meta.get_field('email')
        field_fio = user._meta.get_field('fio')
        field_phone_number = user._meta.get_field('phone_number')
        field_car_type = user._meta.get_field('car_type')
        field_car_model = user._meta.get_field('car_model')
        field_discount = user._meta.get_field('discount')
        field_user_creation_date = user._meta.get_field('user_creation_date')

        self.assertEquals(field_email.verbose_name, 'Логин')
        self.assertEquals(field_email.max_length, 255)
        self.assertEquals(field_fio.verbose_name, 'ФИО')
        self.assertEquals(field_fio.max_length, 255)
        self.assertEquals(field_phone_number.verbose_name, 'телефон')
        self.assertEquals(field_phone_number.max_length, 11)
        self.assertEquals(field_car_type.verbose_name, 'тип автомобиля')
        self.assertEquals(field_car_type.max_length, 40)
        self.assertEquals(field_car_model.verbose_name, 'марка и модель автомобиля')
        self.assertEquals(field_car_model.max_length, 150)
        self.assertEquals(field_discount.verbose_name, 'дисконт')
        self.assertEquals(field_discount.default, 0)
        self.assertEquals(field_user_creation_date.verbose_name, 'дата регистрации пользователя')
        self.assertTrue(field_user_creation_date.auto_now_add)

    def test_user_creation(self):
        # Проверка создания объекта User
        self.assertEqual(self.user.email, 'testuser@mail.ru')
        self.assertEqual(self.user.fio, 'Иванов Пётр Николаевич')
        self.assertEqual(self.user.phone_number, '89445555555')
        self.assertEqual(self.user.car_type, 'price_standart')
        self.assertEqual(self.user.car_model, 'Kia Sportage')
        self.assertEqual(self.user.discount, 0)

    def test_user_get_record(self):
        # Проверка получения записи из бд
        user = User.objects.get(email='testuser@mail.ru')

        self.assertTrue(user)

    def test_user_get_all_records(self):
        # Проверка получения всех записей из бд
        self.assertEqual(User.objects.all().count(), 4)

    def test_user_str(self):
        # Проверка метода __str__()
        self.assertEqual(str(self.user), 'Иванов Пётр Николаевич')
