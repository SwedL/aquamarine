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

    name = models.CharField(max_length=200, verbose_name='название', unique=True, db_index=True)
    process_time = models.SmallIntegerField(default=0, verbose_name='длительность')
    price_standart = models.IntegerField(default=0, verbose_name='седан, хетчбэк')
    price_crossover = models.IntegerField(default=0, verbose_name='кроссовер')
    price_offroad = models.IntegerField(default=0, verbose_name='внедорожник')

    class Meta:
        verbose_name = 'Услугу'
        verbose_name_plural = 'Услуги'
        ordering = ['pk']

    def __str__(self):
        return f'{self.name}'


class CarWashRegistration(models.Model):
    """Модель Регистрация. Поля: пользователь, выбранные услуги"""

    client = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='клиент')
    services = models.ManyToManyField(to=CarWashService, verbose_name='услуги')

    @property
    def total_time(self):
        """Возвращает суммарное время работ регистрации"""
        choice_services = self.services.all()
        time789 = sum([x.pk for x in choice_services if
                       x.pk in [7, 8, 9]]) // 10  # если выбраны улуги, то время берётся как за одну услугу
        overal_time = sum([t.process_time for t in choice_services]) - time789 * 30  # общее время работ

        return overal_time

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        lst_services = ', '.join([str(s) for s in self.services.all()])
        return lst_services
        # return f'{self.client} || {self.client.car_model} || {lst_services}'
    #
    # def all_services(self):
    #     return ', '.join([str(s) for s in self.services.all()])

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super(CarWashRegistration, self).save(force_insert=False, force_update=False, using=None, update_fields=None)


class WorkDay(models.Model):
    """Модель Рабочий день. Поля: дата, остальные поля (время) связь с Регистрация или Null"""

    FORMATTED_KEY = ['date', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                     '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00',
                     '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30'
                     ]

    date = models.DateField(verbose_name='дата', unique=True, db_index=True)
    time_1000 = models.ForeignKey(to=CarWashRegistration, related_name='time1', on_delete=models.SET_NULL, null=True)
    time_1030 = models.ForeignKey(to=CarWashRegistration, related_name='time2', on_delete=models.SET_NULL, null=True)
    time_1100 = models.ForeignKey(to=CarWashRegistration, related_name='time3', on_delete=models.SET_NULL, null=True)
    time_1130 = models.ForeignKey(to=CarWashRegistration, related_name='time4', on_delete=models.SET_NULL, null=True)
    time_1200 = models.ForeignKey(to=CarWashRegistration, related_name='time5', on_delete=models.SET_NULL, null=True)
    time_1230 = models.ForeignKey(to=CarWashRegistration, related_name='time6', on_delete=models.SET_NULL, null=True)
    time_1300 = models.ForeignKey(to=CarWashRegistration, related_name='time7', on_delete=models.SET_NULL, null=True)
    time_1330 = models.ForeignKey(to=CarWashRegistration, related_name='time8', on_delete=models.SET_NULL, null=True)
    time_1400 = models.ForeignKey(to=CarWashRegistration, related_name='time9', on_delete=models.SET_NULL, null=True)
    time_1430 = models.ForeignKey(to=CarWashRegistration, related_name='time10', on_delete=models.SET_NULL, null=True)
    time_1500 = models.ForeignKey(to=CarWashRegistration, related_name='time11', on_delete=models.SET_NULL, null=True)
    time_1530 = models.ForeignKey(to=CarWashRegistration, related_name='time12', on_delete=models.SET_NULL, null=True)
    time_1600 = models.ForeignKey(to=CarWashRegistration, related_name='time13', on_delete=models.SET_NULL, null=True)
    time_1630 = models.ForeignKey(to=CarWashRegistration, related_name='time14', on_delete=models.SET_NULL, null=True)
    time_1700 = models.ForeignKey(to=CarWashRegistration, related_name='time15', on_delete=models.SET_NULL, null=True)
    time_1730 = models.ForeignKey(to=CarWashRegistration, related_name='time16', on_delete=models.SET_NULL, null=True)
    time_1800 = models.ForeignKey(to=CarWashRegistration, related_name='time17', on_delete=models.SET_NULL, null=True)
    time_1830 = models.ForeignKey(to=CarWashRegistration, related_name='time18', on_delete=models.SET_NULL, null=True)
    time_1900 = models.ForeignKey(to=CarWashRegistration, related_name='time19', on_delete=models.SET_NULL, null=True)
    time_1930 = models.ForeignKey(to=CarWashRegistration, related_name='time20', on_delete=models.SET_NULL, null=True)
    time_2000 = models.ForeignKey(to=CarWashRegistration, related_name='time21', on_delete=models.SET_NULL, null=True)
    time_2030 = models.ForeignKey(to=CarWashRegistration, related_name='time22', on_delete=models.SET_NULL, null=True)

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

        # получаем список значений словаря WorkDay только дата и времена
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


class CarWashUserRegistration(models.Model):
    """
    Модель РегистрацияПользователя для отображения записи на странице 'Мои Записи'.
    Поля: пользователь, дата регистрации, время регистрации, связь с Регистрация

    """

    client = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='клиент')
    date_reg = models.DateField(verbose_name='дата записи')
    time_reg = models.TimeField(verbose_name='время записи')
    carwash_reg = models.ForeignKey(to=CarWashRegistration, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Запись пользователя'
        verbose_name_plural = 'Записи пользователей'


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
