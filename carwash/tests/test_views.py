# from datetime import date, time, timedelta
# from http import HTTPStatus
#
# from bs4 import BeautifulSoup
# from django.contrib.auth.models import Permission
# from django.test import TestCase
# from django.urls import reverse
#
# from carwash.models import CarWashRegistration, CarWashService, CarWashWorkDay
# from users.models import User
#
#
# class IndexListViewTestCase(TestCase):
#     """Тест представления главной страницы"""
#
#     fixtures = {'services.json'}
#
#     def setUp(self):
#         self.services = CarWashService.objects.all()
#         self.user = User.objects.create(email='test@mail.ru', password='test')
#         self.permission = Permission.objects.get(codename='view_carwashworkday')
#         self.path = reverse('carwash:home')
#
#     def test_view_for_not_logged_user(self):
#         # Проверка меню для неавторизованных пользователей
#         response = self.client.get(self.path)
#
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertEqual(response.context_data['title'], 'Aquamarine')
#         self.assertTemplateUsed(response, 'carwash/index.html')
#         self.assertEqual(list(response.context_data['object_list']), list(self.services))
#         self.assertEqual(self._common_tests(), [])
#
#     def test_if_logged_but_cannot_permission(self):
#         # Проверка отображения меню для авторизованного пользователя, без permission
#         self.client.force_login(self.user)
#
#         self.assertEqual(self._common_tests(), ['Профиль', 'Мои записи', 'Выйти'])
#
#     def test_if_logged_and_can_permission(self):
#         # Проверка отображения меню для авторизованного пользователя с permission
#         self.user.user_permissions.add(self.permission)
#         self.client.force_login(self.user)
#
#         self.assertEqual(self._common_tests(), ['Профиль', 'Мои записи', 'Сотрудник', 'Выйти'])
#
#     def test_if_logged_and_can_permission_and_is_admin(self):
#         # Проверка отображения меню для авторизованного пользователя, с правами admin
#         self.user.user_permissions.add(self.permission)
#         self.user.is_admin = True
#         self.user.save()
#         self.client.force_login(self.user)
#
#         self.assertEqual(self._common_tests(), ['Профиль', 'Мои записи', 'Сотрудник', 'Админ-панель', 'Выйти'])
#
#     def _common_tests(self):
#         response = self.client.get(self.path)
#
#         soup = BeautifulSoup(response.content, 'html.parser')
#         result = [r.text for r in soup.find_all('a', class_='dropdown-item')]
#         return result
#
#
# class RegistrationAutoViewTestCase(TestCase):
#     """Тест представления страницы записи автомобиля на автомоечный комплекс"""
#
#     fixtures = {'services.json'}
#
#     def setUp(self):
#         self.services = dict([(k, v) for k, v in enumerate(CarWashService.objects.all(), start=1)])
#         self.user = User.objects.create(email='test@mail.ru', password='test')
#         self.workday = CarWashWorkDay.objects.create(date=date.today())
#         self.path = reverse('carwash:registration')
#
#     def test_view(self):
#         response = self.client.get(self.path)
#
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertEqual(response.context['title'], 'Запись автомобиля')
#         self.assertTemplateUsed(response, 'carwash/registration.html')
#         self.assertEqual(list(response.context['services']), list(self.services))
#
#     def test_display_submit_button_for_not_logged_user(self):
#         # Проверка отображения кнопки формы для неавторизованного пользователя
#         self.assertEqual(self._common_tests('call-me__button'), 'Заказать звонок')
#
#     def test_display_submit_button_for_logged_user(self):
#         # Проверка отображения кнопки формы для авторизованного пользователя
#         self.client.force_login(self.user)
#         self.assertEqual(self._common_tests('registration__button'), 'Записаться')
#
#     def test_registration_auto_at_carwash(self):
#         choice_date = str(date.today()).replace('-', ' ')
#         data = {'choice_date_and_time': f'{choice_date},10:00',
#                 'service_1': '1',
#                 }
#         self.client.force_login(self.user)
#         response = self.client.post(self.path, data)
#         check_workday = list(CarWashWorkDay.objects.filter(date=date.today()).values())[0]
#         id_need_carwashregistration = check_workday.get('time_1000_id', False)
#         check_carwashregistration = CarWashRegistration.objects.filter(id=id_need_carwashregistration).first()
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertEqual(check_carwashregistration['total_time'], 60)
#         self.assertEqual(str(check_carwashregistration), 'Мойка (верх, ковры, сушка)')
#         self.assertEqual(str(check_carwashregistration.client), 'test@mail.ru')
#
#     def _common_tests(self, sample):
#         response = self.client.get(self.path)
#         soup = BeautifulSoup(response.content, 'html.parser')
#
#         return soup.find('div', class_=sample).text.strip()
#
#
# # class StaffDetailViewTestCase(TestCase):
# #     """
# #     Тест представления страницы показа сотруднику всех записей клиентов
# #     на оказание услуг автомойки. На сегодня, завтра и послезавтра.
# #     """
# #
# #     def setUp(self):
# #         self.user = User.objects.create(email='test@mail.ru', password='test')
# #         self.permission = Permission.objects.get(codename='view_workday')
# #         self.path = reverse('carwash:staff', kwargs={'days_delta': 0})
# #         [CarWashWorkDay.objects.create(date=date.today() + timedelta(days=i)) for i in range(7)]
# #
# #     def test_user_cannot_permission(self):
# #         # Проверка доступа к странице неавторизованного пользователя
# #         response = self.client.get(self.path)
# #
# #         self.assertEqual(response.status_code, HTTPStatus.FOUND)
# #
# #     def test_user_can_permission(self):
# #         # Проверка доступа к странице авторизованного пользователя
# #         self.user.user_permissions.add(self.permission)
# #         self.client.force_login(self.user)
# #         response = self.client.get(self.path)
# #
# #         self.assertEqual(response.status_code, HTTPStatus.OK)
# #         self.assertEqual(response.context['title'], 'Сотрудник')
# #         self.assertTemplateUsed(response, 'carwash/staff.html')
# #
# #
# # class UserRegistrationsListViewTestCase(TestCase):
# #     """Тест представления показа пользователю его записей на оказание услуг автомойки"""
# #
# #     fixtures = {'services.json'}
# #
# #     def setUp(self):
# #         self.path = reverse('carwash:user_registrations')
# #         self.services = CarWashService.objects.all()
# #
# #         self.user1 = User.objects.create(
# #             email='testuser@mail.ru',
# #             password='12345qwerty',
# #             fio='Иванов Пётр Николаевич',
# #             phone_number='81224567890',
# #             car_model='Kia Sportage',
# #         )
# #         self.user2 = User.objects.create(email='testuser1@mail.ru', password='12345qwerty')
# #
# #         self.registration1 = CarWashRegistration.objects.create(client=self.user1)
# #         self.registration1.services.set([self.services[0], self.services[6]])
# #
# #         self.registration2 = CarWashRegistration.objects.create(client=self.user1)
# #         self.registration2.services.set([self.services[1], self.services[2], self.services[3]])
# #
# #         CarWashRegistration.objects.create(
# #             client=self.user1,
# #             date_reg=date.today(),
# #             time_reg=time(12, 00),
# #             carwash_reg=self.registration1,
# #         )
# #         CarWashRegistration.objects.create(
# #             client=self.user1,
# #             date_reg=date.today(),
# #             time_reg=time(10, 00),
# #             carwash_reg=self.registration2,
# #         )
# #
# #     def test_view(self):
# #         self.client.force_login(self.user1)
# #         response = self.client.get(self.path)
# #
# #         self.assertEqual(response.status_code, HTTPStatus.OK)
# #         self.assertEqual(response.context_data['title'], 'Мои записи')
# #         self.assertTemplateUsed(response, 'carwash/user-registrations.html')
# #
# #     def test_display_user1_registrations(self):
# #         # Проверка корректного отображения всех записей пользователя user1 на странице
# #         self.client.force_login(self.user1)
# #         response = self.client.get(self.path)
# #
# #         self.assertEqual(len(response.context_data['object_list']), 2)
# #
# #     def test_display_user2_registrations(self):
# #         # Проверка корректного отображения всех записей пользователя user2 на странице
# #         self.client.force_login(self.user2)
# #         response = self.client.get(self.path)
# #
# #         self.assertEqual(len(response.context_data['object_list']), 0)
# #
# #
# # class RequestCallFormViewTestCase(TestCase):
# #     """"Тест представления заказа звонка клиенту"""
# #
# #     def setUp(self):
# #         self.path = reverse('carwash:call_me')
# #
# #     def test_view_for_not_logged_user(self):
# #         # Проверка представления страницы заказа звонка
# #         response = self.client.get(self.path)
# #
# #         self.assertEqual(response.status_code, HTTPStatus.OK)
# #         self.assertEqual(response.context_data['title'], 'Заказ звонка')
# #         self.assertTemplateUsed(response, 'carwash/request-call.html')
