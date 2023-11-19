from datetime import date, datetime, time

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from users.models import User


class CarWashService(models.Model):
    """
    Модель Услуга. Поля: название, время необходимое на оказание услуги,
    цена стандарт, цена для кроссоверов, цена для внедорожников
    """

    name = models.CharField(max_length=200, verbose_name='название', unique=True)
    process_time = models.PositiveSmallIntegerField(default=0, verbose_name='длительность')
    price_standart = models.PositiveIntegerField(default=0, verbose_name='седан, хетчбэк')
    price_crossover = models.PositiveIntegerField(default=0, verbose_name='кроссовер')
    price_offroad = models.PositiveIntegerField(default=0, verbose_name='внедорожник')

    class Meta:
        verbose_name = 'Услугу'
        verbose_name_plural = 'Услуги'
        ordering = ['pk']

    def __str__(self):
        return f'{self.name}'


class CarWashRegistration(models.Model):
    """
    Модель РегистрацияПользователя для отображения записи на странице 'Мои Записи'.
    Поля: пользователь, дата регистрации, время регистрации, связь с Регистрация

    """

    client = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='клиент')
    services = models.ManyToManyField(to=CarWashService, verbose_name='услуги')
    date_reg = models.DateField(verbose_name='дата записи')
    time_reg = models.TimeField(verbose_name='время записи')
    total_time = models.PositiveSmallIntegerField(default=0, verbose_name='общее время работ')
    total_cost = models.PositiveIntegerField(default=0, verbose_name='общяя стоимость')
    relation_carwashworkday = models.JSONField(null=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return f'Клиент: {self.client}, {self.client.email}'

    def get_all_services(self):
        return ', '.join(str(i) for i in self.services.all())

    def get_data(self):
        data = {
            'id': self.id,
            'client': str(self.client),
            'email': self.client.email,
            'phone_number': self.client.phone_number,
            'car_model': self.client.car_model,
            'services': [str(i) for i in self.services.all()],
            'total_time': self.total_time,
            'total_cost': self.total_cost,
        }
        return data

# class CarWashRegistration(models.Model):
#     """Модель Регистрация. Поля: пользователь, выбранные услуги"""
#
#     client = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='клиент')
#     services = models.ManyToManyField(to=CarWashService, verbose_name='услуги')
#     total_time = models.PositiveSmallIntegerField(default=0, verbose_name='общее время работ')
#
#     class Meta:
#         verbose_name = 'Запись'
#         verbose_name_plural = 'Записи'
#
#     def __str__(self):
#         lst_services = ', '.join([str(s) for s in self.services.all()])
#         return lst_services

    # def __str__(self):
    #     lst_services = str(self.client) + ' ' + ', '.join([str(s) for s in self.services.all()])
    #     return lst_services

    # def all_services(self):
    #     return ', '.join([str(s) for s in self.services.all()])

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super(CarWashRegistration, self).save(force_insert=False, force_update=False, using=None, update_fields=None)


class CarWashWorkDay(models.Model):
    """Модель Рабочий день. Поля: дата, остальные поля (время) связь с Регистрация или Null"""

    FORMATTED_KEY = ['date', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                     '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00',
                     '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30'
                     ]

    date = models.DateField(verbose_name='дата', unique_for_date=True)
    time_1000 = models.JSONField(default=None, blank=True, null=True)
    time_1030 = models.JSONField(default=None, blank=True, null=True)
    time_1100 = models.JSONField(default=None, blank=True, null=True)
    time_1130 = models.JSONField(default=None, blank=True, null=True)
    time_1200 = models.JSONField(default=None, blank=True, null=True)
    time_1230 = models.JSONField(default=None, blank=True, null=True)
    time_1300 = models.JSONField(default=None, blank=True, null=True)
    time_1330 = models.JSONField(default=None, blank=True, null=True)
    time_1400 = models.JSONField(default=None, blank=True, null=True)
    time_1430 = models.JSONField(default=None, blank=True, null=True)
    time_1500 = models.JSONField(default=None, blank=True, null=True)
    time_1530 = models.JSONField(default=None, blank=True, null=True)
    time_1600 = models.JSONField(default=None, blank=True, null=True)
    time_1630 = models.JSONField(default=None, blank=True, null=True)
    time_1700 = models.JSONField(default=None, blank=True, null=True)
    time_1730 = models.JSONField(default=None, blank=True, null=True)
    time_1800 = models.JSONField(default=None, blank=True, null=True)
    time_1830 = models.JSONField(default=None, blank=True, null=True)
    time_1900 = models.JSONField(default=None, blank=True, null=True)
    time_1930 = models.JSONField(default=None, blank=True, null=True)
    time_2000 = models.JSONField(default=None, blank=True, null=True)
    time_2030 = models.JSONField(default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Рабочий день'
        verbose_name_plural = 'Рабочие дни'

    def __str__(self):
        return f'{self.date}'

    def formatted_dict(self):
        """
        Функция создаёт словарь, где ключи из списка FORMATTED_KEY,
         а значения - значения полей WorkDay (id CarWashRegistration)
         """

        # получаем список значений экземпляра WorkDay только дата и времена
        workday_values = list(self.__dict__.values())[2:]

        # создаём словарь и заменяем не занятые времена, сегодняшнего дня, время которых прошло, на значения "disabled"
        # {'10:00': 'disable', '10:30': None, '11:00': 9, 'date': 2023-10-26}
        res_dict = {}

        if workday_values[0] == date.today():
            for num, k in enumerate(self.FORMATTED_KEY):
                if num != 0 and not workday_values[num] and time(*map(int, k.split(':'))) < datetime.now().time():
                    res_dict[k] = 'disable'
                else:
                    res_dict[k] = workday_values[num]
        else:
            return dict((workday_time, value) for workday_time, value in zip(self.FORMATTED_KEY, workday_values))
        return res_dict


class CarWashRequestCall(models.Model):
    """Модель Запроса Звонка. Поля: номер телефона, обработан или нет, DateTime создания"""

    phone_regex = RegexValidator(regex=r'8\d{10}$',
                                 message='Номер телефона должен быть в формате: "89999999999"')

    phone_number = models.CharField(validators=[phone_regex], max_length=11, verbose_name='номер телефона')
    processed = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now, verbose_name='создан')

    class Meta:
        verbose_name = 'Request Call'
        verbose_name_plural = 'Request Call'

    def __str__(self):
        return f'{str(self.created.time())[0:5]} --- {self.phone_number}'

# python manage.py shell
