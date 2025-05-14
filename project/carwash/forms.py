from captcha.fields import CaptchaField
from django import forms
from django.core.validators import RegexValidator


class CarWashRequestCallForm(forms.Form):
    """Форма RequestCall (заказать звонок)"""

    phone_regex = RegexValidator(regex=r'8\d{10}',
                                 message='Номер телефона должен быть в формате: "89999999999"')
    phone_number = forms.CharField(validators=[phone_regex], max_length=11,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control py-4',
                                           'autocomplete': 'on',
                                           'id': 'phone',
                                           'placeholder': 'номер телефона',
                                       })
                                   )
    captcha = CaptchaField()
