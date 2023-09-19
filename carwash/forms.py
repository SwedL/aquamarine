from django import forms
from django.core.validators import RegexValidator


class CarwashRequestCallForm(forms.Form):
    """Создание объекта модели RequestCall (заказать звонок)"""

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$',
                                 message="Номер телефона должен быть в формате: '89999999999' или '+79999999999'")
    phone_number = forms.CharField(validators=[phone_regex], max_length=12,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control py-4', 'autocomplete': 'off',
                                              'placeholder': 'номер телефона'})
                                   )

