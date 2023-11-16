from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
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
    Модель Пользователь.
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
    REQUIRED_FIELDS = []  # field required to createsuperuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __str__(self):
        return self.email
