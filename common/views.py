from datetime import date, timedelta

from carwash.models import WorkDay

menu_navigation = [{'title': 'Главная', 'url_name': 'carwash:home'},
                   {'title': 'Доступное время', 'url_name': 'carwash:registration'},
                   {'title': 'Услуги и цены', 'anchor': '#services_price'},
                   {'title': 'Контакты и адрес', 'anchor': '#footer'},
                   ]


def create_week_workday():
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
    # staff = False

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
