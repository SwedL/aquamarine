from django.test import TestCase

from users.models import User


class UserModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@mail.ru', password='12345qwerty', fio='Иванов Пётр Николаевич',
                                        phone_number='+79445555555', car_model='Kia Sportage')
        User.objects.create(email='testuser2@mail.ru', password='12345qwerty')
        User.objects.create(email='testuser3@mail.ru', password='12345qwerty')
        User.objects.create(email='testuser4@mail.ru', password='12345qwerty')
        self.get_user = User.objects.get(id=1)

    def test_email_label(self):
        field_label = self.get_user._meta.get_field('email').verbose_name
        max_length = self.get_user._meta.get_field('email').max_length
        self.assertEquals(field_label, 'Логин')
        self.assertEquals(max_length, 255)

    def test_fio_label(self):
        field_label = self.get_user._meta.get_field('fio').verbose_name
        max_length = self.get_user._meta.get_field('email').max_length
        self.assertEquals(field_label, 'ФИО')
        self.assertEquals(max_length, 255)

    def test_phone_number_label(self):
        field_label = self.get_user._meta.get_field('phone_number').verbose_name
        max_length = self.get_user._meta.get_field('phone_number').max_length
        self.assertEquals(field_label, 'телефон')
        self.assertEquals(max_length, 11)

    def test_car_type_label(self):
        field_label = self.get_user._meta.get_field('car_type').verbose_name
        max_length = self.get_user._meta.get_field('car_type').max_length
        self.assertEquals(field_label, 'тип автомобиля')
        self.assertEquals(max_length, 40)

    def test_car_model_label(self):
        field_label = self.get_user._meta.get_field('car_model').verbose_name
        max_length = self.get_user._meta.get_field('car_model').max_length
        self.assertEquals(field_label, 'марка и модель автомобиля')
        self.assertEquals(max_length, 150)

    def test_discount_label(self):
        field_label = self.get_user._meta.get_field('discount').verbose_name
        default_value = self.get_user._meta.get_field('discount').default
        self.assertEquals(field_label, 'дисконт')
        self.assertEquals(default_value, 0)

    def test_user_creation_date_label(self):
        field_label = self.get_user._meta.get_field('user_creation_date').verbose_name
        add_field = self.get_user._meta.get_field('user_creation_date').auto_now_add
        self.assertEquals(field_label, 'дата регистрации пользователя')
        self.assertTrue(add_field)

    def test_user_creation(self):
        # Проверка создания объекта User
        self.assertEqual(self.user.email, 'testuser@mail.ru')
        self.assertEqual(self.user.fio, 'Иванов Пётр Николаевич')
        self.assertEqual(self.user.phone_number, '+79445555555')
        self.assertEqual(self.user.car_type, 'price_standart')
        self.assertEqual(self.user.car_model, 'Kia Sportage')
        self.assertEqual(self.user.discount, 0)

    def test_user_get_record(self):
        # Проверка получения записи из бд
        user = User.objects.get(email='testuser@mail.ru')

        self.assertTrue(user)

    def test_user_get_all_records(self):
        # Проверка получения всех записей из бд
        users = User.objects.all()
        self.assertEqual(len(users), 4)

    def test_user_str(self):
        # Проверка метода __str__()
        expected_str = 'testuser@mail.ru'
        self.assertEqual(str(self.user), expected_str)

