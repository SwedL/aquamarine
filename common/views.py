from datetime import date, time, timedelta
from itertools import dropwhile

from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render

# from api.views import CarWashRegistrationAPIView
from carwash.models import WorkDay, CarWashService, CarWashRegistration, CarWashUserRegistration

menu_navigation = [{'title': 'Главная', 'url_name': 'carwash:home'},
                   {'title': 'Доступное время', 'url_name': 'carwash:registration'},
                   {'title': 'Услуги и цены', 'anchor': '#services_price'},
                   {'title': 'Контакты и адрес', 'anchor': '#footer'},
                   ]

FORMATTED_KEY = ['date', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                 '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00',
                 '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']


def create_and_get_week_workday():
    dates_week = [date.today() + timedelta(days=i) for i in range(7)]

    check_objects = WorkDay.objects.filter(date__in=dates_week).order_by('date')
    if len(check_objects) < 7:
        for day_ in dates_week:  # создаём день (объект WorkDay), если его нет в БД
            if not WorkDay.objects.filter(date=day_).exists():
                WorkDay.objects.create(date=day_)
        check_objects = WorkDay.objects.filter(date__in=dates_week).order_by('date')

    return check_objects


class Common:
    FORMATTED_KEY = ['date', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                     '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00',
                     '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']

    title = 'Aquamarine'
    menu = range(3)

    @classmethod
    def create_menu(cls, menu):
        for i in menu:
            assert 0 <= i < len(menu_navigation)

        return [menu_navigation[i] for i in menu]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Common, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['menu'] = self.create_menu(self.menu)
        context['staff'] = self.request.user.has_perm('carwash.view_workday')

        return context


class RegistrationMixin(Common):
    def get(self, request):
        # проверяем наличие объектов WorkDay на неделю вперёд и получаем их из функции
        objects_week_workday = create_and_get_week_workday()

        # удаляем экземпляры WorkDay если они старше 1 года
        WorkDay.objects.filter(date__lt=date.today() - timedelta(days=365)).delete()

        # создаём словарь где ключи это id услуги, а значение, сама услуга
        services = dict([(service.pk, service) for service in CarWashService.objects.all().order_by('id')])

        # получаем список из словарей значений WorkDay
        # {'date': datetime.date(2023, 10, 24), '10:00': 'disable', '10:30': 3, '11:00': 3, ...}
        # где key - время, value - CarWashRegistration.id либо 'disabled' если время прошло, None если время актуально
        list_day_dictionaries = list(map(lambda i: i.formatted_dict(), objects_week_workday))

        context = {
            'title': 'Запись автомобиля',
            'menu': self.create_menu((0,)),
            'staff': request.user.has_perm('carwash.view_workday'),
            'services': services,
            'list_day_dictionaries': list_day_dictionaries,
        }

        return render(request, 'carwash/registration.html', context=context)

    def post(self, request):
        choicen_date, choicen_time = request.POST['choice_date_and_time'].split(',')
        choicen_services_list_pk = list(
            map(lambda i: int(i.split('_')[1]), filter(lambda x: x.startswith('service'), request.POST))
        )
        choicen_services = CarWashService.objects.filter(pk__in=choicen_services_list_pk)
        total_cost = sum(getattr(x, request.user.car_type) for x in choicen_services)

        # проверяем если ранее User создавал такую же CarWashRegistration с теми же услугами, то используем её.
        all_registrations_user = CarWashRegistration.objects.filter(client=request.user).prefetch_related('services')

        for reg in all_registrations_user:
            if choicen_services == list(reg.services.all()):
                new_reg = reg
                break
        else:
            new_reg = CarWashRegistration(client=request.user)  # создаём CarWashRegistration от пользователя
            new_reg.save()
            new_reg.services.set(choicen_services)  # добавляем в CarWashRegistration выбранные услуги

            # вычисляем общее время работ total_time в CarWashRegistration (7,8,9 считается как за одно время 30 мин.)
            choice_services = new_reg.services.all()
            time789 = sum([x.pk for x in choice_services if
                           x.pk in [7, 8, 9]]) // 10  # если выбраны улуги, то время берётся как за одну услугу
            new_reg.total_time = sum([t.process_time for t in choice_services]) - time789 * 30
            new_reg.save()

        total_time = new_reg.total_time

        for_workday_date = date(*map(int, choicen_date.split()))  # дата которую выбрал клиент
        for_workday_time = time(*map(int, choicen_time.split(':')))  # время которое выбрал клиент
        current_workday = WorkDay.objects.get(date=for_workday_date)

        # записываем столько времён под авто, сколько необходимо под услуги
        # из списка времен FORMATTED_KEY выбираем от choicen_time и далее
        formatted_key1 = list(dropwhile(lambda el: el != choicen_time, self.FORMATTED_KEY))
        formatted_key2 = formatted_key1.copy()

        # Если время выбранное всё ещё свободно пока пользователь делал свой выбор,
        # то сохраняем CarWashRegistration, если занято пока проходило оформление,
        # то сообщаем "К сожалению, время которые вы выбрали уже занято"
        check_free_times = [getattr(current_workday, 'time_' + formatted_key2.pop(0).replace(':', '')) for _ in
                            range(0, total_time, 30)]

        if all([x is None for x in check_free_times]):
            for _ in range(0, total_time, 30):
                setattr(current_workday, 'time_' + formatted_key1.pop(0).replace(':', ''),
                        new_reg)  # в поле соответствующего времени сохраняем CarWashRegistration
            current_workday.save()

            # создаём CarWashUserRegistration - запись пользователя для отслеживания в "Мои записи"
            CarWashUserRegistration.objects.create(
                client=request.user,
                date_reg=for_workday_date,
                time_reg=for_workday_time,
                carwash_reg=new_reg,
            )
        else:
            context = {
                'title': 'Ошибка записи',
                'menu': self.create_menu((0, 1)),
                'staff': request.user.has_perm('carwash.view_workday'),
            }
            if 'api' in str(request):
                return context

            return render(request, 'carwash/registration-error.html', context=context)

        normal_format_choicen_date = choicen_date.split()  # создаём список данных из выбранной даты "2023 09 10"
        normal_format_choicen_date.reverse()  # разворачиваем список для удобного вывода информации пользователю

        normal_total_time = f'{total_time // 60} ч.  {total_time - total_time // 60 * 60} мин.'

        context = {
            'title': 'Запись зарегистрирована',
            'menu': self.create_menu((0,)),
            'staff': request.user.has_perm('carwash.view_workday'),
            'normal_format_choicen_date': '/'.join(normal_format_choicen_date),
            'choice_time': choicen_time,
            'choice_services': choicen_services,
            'total_time': normal_total_time,
            'total_cost': f'{total_cost} р.',
        }
        if 'api' in str(request):
            return context
        return render(request, 'carwash/registration-done.html', context=context)


def carwash_user_registration_delete(request, registration_pk):
    """
    Функция для UserRegistrationsCancelView и CarWashUserRegistrationAPIView - обработчик события
    'отмены (удаления)' пользователем своей записи
     """
    user_registration = CarWashUserRegistration.objects.filter(pk=registration_pk).first()

    # проверка что пользователь удаляет принадлежащую ему CarWashUserRegistration
    if not user_registration or user_registration.client != request.user:
        raise Http404

    needed_workday = WorkDay.objects.get(date=user_registration.date_reg)
    needed_staff_registration = CarWashRegistration.objects.get(pk=user_registration.carwash_reg.pk)
    total_time = needed_staff_registration.total_time
    time_without_sec = str(user_registration.time_reg)[:-3]  # убираем значения секунд во времени записи '10:00'

    # создаём список времён от времени регистрации user_registration.time_reg и все времена после
    formatted_key = list(dropwhile(lambda el: el != time_without_sec, FORMATTED_KEY.copy()))

    # определяем начальный атрибут (time_....) необходимого объекта WorkWay удаляемой "Записи"
    attr_first_time = 'time_' + formatted_key.pop(0).replace(':', '')

    # определяем CarWashRegistration в найденном времени-поля, если она есть
    first_time_registration = getattr(needed_workday, attr_first_time, None)

    # если в поле WorkDay вообще присутствует CarWashRegistration
    # и её клиент соответствует текущему пользователю, то удаляем в этом поле WorkDay CarWashRegistration,
    # а затем, в следующих полях сколько требовалось времён-полей под услуги CarWashRegistration
    if first_time_registration and first_time_registration.client == request.user:
        setattr(needed_workday, attr_first_time, None)
        # удаляем записи выбранной CarWashRegistration в полях времени,
        # сколько она занимает времен объекта WorkDay - 30 т.к. начальное время мы уже удалили выше
        for _ in range(0, total_time - 30, 30):
            setattr(needed_workday, 'time_' + formatted_key.pop(0).replace(':', ''),
                    None)  # значению поля соотвествующего времени присваиваем значение None (как по умолчанию)
        needed_workday.save()

    # удаляем CarWashUserRegistration пользователя
    user_registration.delete()
