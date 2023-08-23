from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    STANDART = 'price_standart'
    CROSSOVER = 'price_crossover'
    OFFROAD = 'price_offroad'
    MODEL_CHOICES = [
        (STANDART, 'седан, хетчбэк'),
        (CROSSOVER, 'кроссовер'),
        (OFFROAD, 'внедорожник'),
    ]

    username = models.EmailField(max_length=255, verbose_name="login", unique=True)
    fio = models.CharField(max_length=255, blank=True, verbose_name='ФИО')
    tel = models.CharField(max_length=15, blank=True, verbose_name='телефон')
    car_type = models.CharField(max_length=40, choices=MODEL_CHOICES, default=STANDART, verbose_name='тип автомобиля')
    car_model = models.CharField(max_length=150, blank=True, verbose_name='марка и модель автомобиля')
    discount = models.SmallIntegerField(default=0, verbose_name='дисконт')

