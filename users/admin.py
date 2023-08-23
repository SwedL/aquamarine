from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User
from django.contrib.auth.models import Group
from carwash.admin import CarWashRegistrationAdmin
from django.utils.translation import gettext_lazy as _


# admin.site.unregister(User)
# # admin.site.register(User)
# admin.site.register(User, UserAdmin)


class UserAdmin(BaseUserAdmin):
    list_display = ("username", "fio")
    readonly_fields = ("date_joined", )
    fieldsets = [
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("fio", "car_type", "car_model", "tel", "discount", "date_joined")}),
        (_("Permissions"), {"fields": ("is_active", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    ]
    inlines = (CarWashRegistrationAdmin,)


admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)
