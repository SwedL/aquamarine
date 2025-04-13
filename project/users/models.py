from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from users.permissions import staff_permission


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Создает и сохраняет пользователя с указанным адресом
         электронной почты и паролем.
        """
        if not email:
            raise ValueError('Пользователи должны иметь адрес электронной почты')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Создает и сохраняет суперпользователя с указанным адресом
         электронной почты и паролем.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель Пользователь
    Поля: email (login), ФИО, номер телефона, тип автомобиля,
    марка и модель, дисконт, DateTime создания пользователя
    """

    STANDART = 'price_standart'
    CROSSOVER = 'price_crossover'
    OFFROAD = 'price_offroad'
    MODEL_CHOICES = [
        (STANDART, 'седан, хетчбэк'),
        (CROSSOVER, 'кроссовер'),
        (OFFROAD, 'внедорожник'),
    ]

    email = models.EmailField(max_length=255, verbose_name='Логин', unique=True)
    fio = models.CharField(max_length=255, blank=True, verbose_name='ФИО')
    phone_number = models.CharField(max_length=11, blank=True, verbose_name='телефон')
    car_type = models.CharField(max_length=40, choices=MODEL_CHOICES, default=STANDART, verbose_name='тип автомобиля')
    car_model = models.CharField(max_length=150, blank=True, verbose_name='марка и модель автомобиля')
    discount = models.SmallIntegerField(default=0, verbose_name='дисконт')
    user_creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации пользователя')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # поле, необходимое для создания суперпользователя

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def has_perm(self, perm, obj=None):
        """Имеет ли пользователь определенное разрешение?"""
        # Самый простой ответ: Да, всегда.
        if self.is_admin:
            return True
        return super(AbstractBaseUser, self).has_perm(perm)

    def has_module_perms(self, app_label):
        """Есть ли у пользователя разрешения на просмотр приложения app_label?"""
        # Самый простой ответ: Да, всегда.
        return self.is_admin

    @property
    def is_staff(self):
        """Является ли пользователь сотрудником?"""
        # Самый простой ответ: все администраторы — сотрудники.
        if self.is_admin:
            return True
        return super(AbstractBaseUser, self).has_perm(staff_permission)

    def __str__(self):
        return self.fio
