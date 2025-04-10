from datetime import date, datetime, time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from users.models import User


class CarWashService(models.Model):
    """Модель Услуга"""

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
    Модель регистрация автомобиля пользователя на автомоечный комплекс.
    Поля: пользователь,
          услуги,
          дата регистрации,
          время регистрации,
          общее время работ,
          общая стоимость,
          JSON объект содержит {'time_attributes':  ["time_1030", "time_1100"]},
             атрибуты времени занятые записью в CarWashWorkDay
    """

    client = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='клиент')
    services = models.ManyToManyField(to=CarWashService, verbose_name='услуги')
    date_reg = models.DateField(verbose_name='дата записи')
    time_reg = models.TimeField(verbose_name='время записи')
    total_time = models.PositiveSmallIntegerField(default=0, verbose_name='общее время работ')
    total_cost = models.PositiveIntegerField(default=0, verbose_name='общая стоимость')
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


class CarWashWorkDay(models.Model):
    """
    Модель Рабочий день.
    Поля: дата,
          остальные поля (время) - JSON объект с данными CarWashRegistration или Null
    """

    FORMATTED_KEY = ['date', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                     '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00',
                     '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30'
                     ]

    date = models.DateField(verbose_name='дата', unique=True)
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
        а значения - значения полей экземпляра модели CarWAshWorkDay
           ('disable' - если время уже не актуально либо None либо JSON объект данных CarWashRegistration)
        """

        # получаем список значений экземпляра WorkDay только дата и времена
        workday_values = list(self.__dict__.values())[2:]

        # создаём словарь и заменяем не занятые времена, сегодняшнего дня, время которых прошло, на значения "disabled"
        # {
        #  '10:00': 'disable',
        #  '10:30': None,
        #  '11:00': {'id': 1, 'client': 'Elon Musk', ..., 'total_cost': 1150},
        #  'date': 2023-10-26,
        # }

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
    """
    Модель Запроса Звонка.
    Поля: номер телефона,
          обработан или нет,
          DateTime создания
    """

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


def carwash_workday_or_request_call_post_save(sender, instance, signal, *args, **kwargs):
    # После появления новой записи клиента на услуги автомойки или появления
    # нового запроса звонка, отправляется сообщение по протоколу Websocket,
    # на страницу интерфейса сотрудника и она перезагружается
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("staff_group", {"type": "staff_message", "message": 'update_data'})


models.signals.post_save.connect(carwash_workday_or_request_call_post_save, sender=CarWashRequestCall)
models.signals.post_save.connect(carwash_workday_or_request_call_post_save, sender=CarWashWorkDay)

# python manage.py shell
