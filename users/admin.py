from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from carwash.admin import CarWashRegistrationAdmin

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'is_admin']


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'fio', 'car_type', 'phone_number', 'is_admin']
    list_filter = ['is_admin']
    readonly_fields = ['user_creation_date', 'last_login']
    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        (_('Personal info'),
         {'fields': ['fio', 'car_type', 'car_model', 'phone_number', 'discount', 'user_creation_date', 'last_login']}),
        (_('Permissions'), {'fields': ['is_admin', 'is_active', 'groups']}),
        # (_('Important dates'), {'fields': ('last_login',)}),
    ]
    inlines = (CarWashRegistrationAdmin,)

    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['email', 'password1', 'password2'],
        },
         ),
    ]
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = (
        'groups',
        'user_permissions',
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
