from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, SetPasswordForm,
                                       UserChangeForm, password_validation)
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from users.models import User


class UserLoginForm(AuthenticationForm):
    """Форма авторизация пользователя"""
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Электронная почта'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(UserChangeForm):
    """Форма профиля пользователя для изменения данных"""

    STANDART = 'price_standart'
    CROSSOVER = 'price_crossover'
    OFFROAD = 'price_offroad'
    MODEL_CHOICES = [
        (STANDART, 'седан, хетчбэк'),
        (CROSSOVER, 'кроссовер'),
        (OFFROAD, 'внедорожник'),
    ]
    phone_regex = RegexValidator(regex=r'8\d{10}',
                                 message='Номер телефона должен быть в формате: "89999999999"')

    email = forms.EmailField(label='Логин', max_length=255,
                             widget=forms.EmailInput(attrs={'class': 'readonly', 'readonly': 'True'}))
    fio = forms.CharField(label='ФИО', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(validators=[phone_regex], max_length=11,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'autocomplete': 'on',
                                              'placeholder': 'номер телефона'})
                                   )
    # car_type = forms.ChoiceField(label='Тип автомобиля', choices=MODEL_CHOICES,
    #                              widget=forms.TextInput(attrs={'class': 'readonly', 'readonly': 'True'}))
    car_model = forms.CharField(label='Марка и модель автомобиля',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    discount = forms.IntegerField(label='Дисконт', min_value=0, max_value=50,
                                  widget=forms.TextInput(attrs={'class': 'readonly', 'readonly': 'True'}))

    class Meta:
        model = User
        fields = ('email', 'fio', 'phone_number', 'car_model', 'discount',)


class MyPasswordChangeForm(PasswordChangeForm):
    """Форма смены пароля пользователя"""

    old_password = forms.CharField(
        label=_('Old password'),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'form-control', 'autofocus': True}
        ),
    )
    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_('New password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('password1', 'password2')


class UserForgotPasswordForm(PasswordResetForm):
    """Форма запроса на восстановление пароля"""

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={'class': 'form-control py-4', 'autocomplete': 'off', 'placeholder': 'Электронная почта'}),
    )


class UserSetNewPasswordForm(SetPasswordForm):
    """Форма для установки нового пароля пользователя по ссылке на эл.почте"""

    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_('New password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control'}),
    )
