# from datetime import date, time, timedelta
# from itertools import dropwhile
#
# from django.contrib.auth.mixins import (LoginRequiredMixin,
#                                         PermissionRequiredMixin)
# from carwash.models import CarWashService
#
# class RegistrationAutoPostService:
#     def get_context(self):
#         if request.POST:
#             choicen_date, choicen_time = request.POST['choice_date_and_time'].split(',')
#             choicen_services_ids = list(
#                 map(lambda i: int(request.POST[i]), filter(lambda x: x.startswith('service'), request.POST))
#             )
#             choicen_services = CarWashService.objects.filter(pk__in=choicen_services_ids)
#         else:
#             choicen_date, choicen_time = request.data['choice_date_and_time'].split(',')
#             choicen_services = CarWashService.objects.filter(pk__in=request.data['services_list'])
#
#         total_cost = sum(getattr(x, request.user.car_type) for x in choicen_services)
#
#         for_workday_date = date(*map(int, choicen_date.split()))  # дата, которую выбрал клиент
#         for_workday_time = time(*map(int, choicen_time.split(':')))  # время, которое выбрал клиент
#
#         # вычисляем общее время работ total_time в CarWashRegistration (7,8,9 считается как за одно время 30 мин.)
#         time789 = sum([x.pk for x in choicen_services if
#                        x.pk in [7, 8, 9]]) // 10  # если выбраны услуги, то время берётся как за одну услугу
#         total_time = sum([t.process_time for t in choicen_services]) - time789 * 30
#         current_workday = CarWashWorkDay.objects.filter(date=for_workday_date).first()
#
#         # записываем столько времён под авто, сколько необходимо под услуги
#         # из списка времен FORMATTED_KEY выбираем от choicen_time и далее
#         time_dict1 = list(dropwhile(lambda el: el != choicen_time, FORMATTED_KEY))
#         time_dict2 = time_dict1.copy()
#
#         # Если время выбранное всё ещё свободно пока пользователь делал свой выбор,
#         # то сохраняем CarWashRegistration, если стало занято, пока проходило оформление,
#         # то сообщаем "К сожалению, время которые вы выбрали уже занято" и отменяем запись
#         check_free_times = [getattr(current_workday, 'time_' + time_dict2.pop(0).replace(':', '')) for _ in
#                             range(0, total_time, 30)]
#
#         if all([x is None for x in check_free_times]):
#             new_reg = CarWashRegistration.objects.create(
#                 client=request.user,
#                 date_reg=for_workday_date,
#                 time_reg=for_workday_time,
#                 total_time=total_time,
#                 total_cost=total_cost,
#             )
#             new_reg.services.set(choicen_services)  # добавляем в CarWashRegistration выбранные услуги
#             time_attributes = []
#             self_data = new_reg.get_data()  # получаем данные CarWashRegistration в виде словаря
#
#             # если записывает сотрудник, то берутся данные 'comment_...'
#             match request.POST:
#                 case {'comment_car_model': car_model, 'comment_phone_number': phone_number, 'comment_client': client}:
#                     self_data['car_model'] = car_model
#                     self_data['phone_number'] = phone_number
#                     self_data['client'] = client
#
#             for _ in range(0, total_time, 30):
#                 time_attribute = 'time_' + time_dict1.pop(0).replace(':', '')
#                 time_attributes.append(time_attribute)
#                 # в поле соответствующего времени сохраняем JSON объект данных CarWashRegistration
#                 setattr(current_workday, time_attribute, self_data)
#             current_workday.save()
#             new_reg.relation_carwashworkday = {'time_attributes': time_attributes}
#             new_reg.save()
#
#         else:
#             context = {
#                 'title': 'Ошибка записи',
#                 'menu': self.create_menu((0, 1)),
#                 'staff': request.user.has_perm('carwash.view_carwashworkday'),
#             }
#
#             # Если запрос поступил по API, то возвращаем только данные (context)
#             if self.request.META.get('PATH_INFO', '/registration/') == '/api/v1/carwash-registration/':
#                 return context
#
#             return render(request, 'carwash/registration-error.html', context=context)
#
#         normal_format_choicen_date = choicen_date.split()  # создаём список данных из выбранной даты "2023 09 10"
#         normal_format_choicen_date.reverse()  # разворачиваем список для удобного вывода информации пользователю
#
#         normal_total_time = f'{total_time // 60} ч.  {total_time - total_time // 60 * 60} мин.'
#
#         context = {
#             'title': 'Запись зарегистрирована',
#             'menu': self.create_menu((0,)),
#             'staff': request.user.has_perm('carwash.view_carwashworkday'),
#             'normal_format_choicen_date': '/'.join(normal_format_choicen_date),
#             'choice_time': choicen_time,
#             'choice_services': choicen_services,
#             'total_time': normal_total_time,
#             'total_cost': f'{total_cost} р.',
#         }
#
#         if request.user.has_perm('carwash.view_carwashworkday'):
#             context.get('menu').append({'title': 'Менеджер', 'url_name': 'carwash:staff'})
#
#         # Если запрос поступил по API, то возвращаем только данные (context)
#         if self.request.META.get('PATH_INFO', '/registration/') == '/api/v1/carwash-registration/':
#             return context
