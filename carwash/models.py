from django.db import models
from django.conf import settings
from users.models import User


class CarWashService(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='название', unique=True)
    process_time = models.SmallIntegerField(default=0, verbose_name='длительность')
    price_standart = models.IntegerField(default=0, verbose_name='седан, хетчбэк')
    price_crossover = models.IntegerField(default=0, verbose_name='кроссовер')
    price_offroad = models.IntegerField(default=0, verbose_name='внедорожник')

    class Meta:
        verbose_name = "Услугу"
        verbose_name_plural = "Услуги"
        ordering = ['pk']

    def __str__(self):
        return f'{self.name}'


class CarWashRegistration(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="клиент")
    services = models.ManyToManyField(CarWashService, verbose_name="услуги")

    def total_time_reg(self):
        "Возвращает суммарное время работ регистрации"
        choice_services = self.services.all()
        time789 = sum([x.pk for x in choice_services if x.pk in [7, 8, 9]]) // 10  # если выбраны улуги, то время берётся как за одну
        overal_time = sum([t.process_time for t in choice_services]) - time789 * 30  # общее время работ

        return overal_time

    total_time = property(total_time_reg)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        lst_services = ', '.join([str(s) for s in self.services.all()])
        return f'{self.client} || {self.client.car_model} || {lst_services}'


class WorkDay(models.Model):
    date = models.DateField(verbose_name='дата')
    time_1000 = models.ForeignKey(CarWashRegistration, related_name='example1', on_delete=models.SET_NULL, null=True, blank=True)
    time_1030 = models.ForeignKey(CarWashRegistration, related_name='example2', on_delete=models.SET_NULL, null=True, blank=True)
    time_1100 = models.ForeignKey(CarWashRegistration, related_name='example3', on_delete=models.SET_NULL, null=True, blank=True)
    time_1130 = models.ForeignKey(CarWashRegistration, related_name='example4', on_delete=models.SET_NULL, null=True, blank=True)
    time_1200 = models.ForeignKey(CarWashRegistration, related_name='example5', on_delete=models.SET_NULL, null=True, blank=True)
    time_1230 = models.ForeignKey(CarWashRegistration, related_name='example6', on_delete=models.SET_NULL, null=True, blank=True)
    time_1300 = models.ForeignKey(CarWashRegistration, related_name='example7', on_delete=models.SET_NULL, null=True, blank=True)
    time_1330 = models.ForeignKey(CarWashRegistration, related_name='example8', on_delete=models.SET_NULL, null=True, blank=True)
    time_1400 = models.ForeignKey(CarWashRegistration, related_name='example9', on_delete=models.SET_NULL, null=True, blank=True)
    time_1430 = models.ForeignKey(CarWashRegistration, related_name='example10', on_delete=models.SET_NULL, null=True, blank=True)
    time_1500 = models.ForeignKey(CarWashRegistration, related_name='example11', on_delete=models.SET_NULL, null=True, blank=True)
    time_1530 = models.ForeignKey(CarWashRegistration, related_name='example12', on_delete=models.SET_NULL, null=True, blank=True)
    time_1600 = models.ForeignKey(CarWashRegistration, related_name='example13', on_delete=models.SET_NULL, null=True, blank=True)
    time_1630 = models.ForeignKey(CarWashRegistration, related_name='example14', on_delete=models.SET_NULL, null=True, blank=True)
    time_1700 = models.ForeignKey(CarWashRegistration, related_name='example15', on_delete=models.SET_NULL, null=True, blank=True)
    time_1730 = models.ForeignKey(CarWashRegistration, related_name='example16', on_delete=models.SET_NULL, null=True, blank=True)
    time_1800 = models.ForeignKey(CarWashRegistration, related_name='example17', on_delete=models.SET_NULL, null=True, blank=True)
    time_1830 = models.ForeignKey(CarWashRegistration, related_name='example18', on_delete=models.SET_NULL, null=True, blank=True)
    time_1900 = models.ForeignKey(CarWashRegistration, related_name='example19', on_delete=models.SET_NULL, null=True, blank=True)
    time_1930 = models.ForeignKey(CarWashRegistration, related_name='example20', on_delete=models.SET_NULL, null=True, blank=True)
    time_2000 = models.ForeignKey(CarWashRegistration, related_name='example21', on_delete=models.SET_NULL, null=True, blank=True)
    time_2030 = models.ForeignKey(CarWashRegistration, related_name='example22', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Рабочий день"
        verbose_name_plural = "Рабочие дни"

    def __str__(self):
        return f'{self.date}'
