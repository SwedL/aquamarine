from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, password_validation
from django import forms
from users.models import User

# gettext_lazy = lazy(gettext, str)


class UserLoginForm(AuthenticationForm):
    """Авторизация пользователя"""
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Электронная почта'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Пароль'}))

    # class Meta:
    #     model = User
    #     fields = ('username', 'password')


class UserProfileForm(UserChangeForm):
    """Создание нового пользователя"""

    STANDART = 'price_standart'
    CROSSOVER = 'price_crossover'
    OFFROAD = 'price_offroad'
    MODEL_CHOICES = [
        (STANDART, 'седан, хетчбэк'),
        (CROSSOVER, 'кроссовер'),
        (OFFROAD, 'внедорожник'),
    ]

    email = forms.EmailField(label='Логин', max_length=255, widget=forms.EmailInput(attrs={'class': 'readonly', 'readonly': 'True'}))
    fio = forms.CharField(label='ФИО', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tel = forms.CharField(label='Телефон', max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    car_type = forms.ChoiceField(label='Тип автомобиля', choices=MODEL_CHOICES, widget=forms.TextInput(attrs={'class': 'readonly', 'readonly': 'True'}))
    car_model = forms.CharField(label='Марка и модель автомобиля', widget=forms.TextInput(attrs={'class': 'form-control'}))
    discount = forms.IntegerField(label='Дисконт', widget=forms.TextInput(attrs={'class': 'readonly', 'readonly': 'True'}))

    class Meta:
        model = User
        fields = ('email', 'fio', 'tel', 'car_type', 'car_model', 'discount',)


class MyPasswordChangeForm(PasswordChangeForm):
    """Смена пароля пользователя"""
    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", 'class': 'form-control', "autofocus": True}
        ),
    )

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('password1', 'password2',)


class UserForgotPasswordForm(PasswordResetForm):
    """Запрос на восстановление пароля"""

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы"""

        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UserSetNewPasswordForm(SetPasswordForm):
    """Изменение пароля пользователя после подтверждения"""

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы"""

        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


