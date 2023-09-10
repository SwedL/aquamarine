from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Электронная почта'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Пароль'}))

    # class Meta:
    #     model = User
    #     fields = ('username', 'password')


class UserProfileForm(UserChangeForm):
    email = forms.EmailField(label='Логин', widget=forms.EmailInput(attrs={'class': 'readonly', 'readonly': 'True'}))
    fio = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-control'}))
    tel = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # car_type = forms.ChoiceField(label='Тип автомобиля', widget=forms.TextInput(attrs={'class': 'readonly', 'readonly': 'True'}))
    car_model = forms.CharField(label='Марка и модель автомобиля', widget=forms.TextInput(attrs={'class': 'form-control'}))
    discount = forms.IntegerField(label='Дисконт', widget=forms.TextInput(attrs={'class': 'readonly', 'readonly': 'True'}))

    class Meta:
        model = User
        fields = ('email', 'fio', 'tel', 'car_type', 'car_model', 'discount', )


