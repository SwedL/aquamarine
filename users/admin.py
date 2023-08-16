from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from django.contrib.auth.models import Group
from carwash.admin import CarWashRegistrationAdmin


# admin.site.unregister(User)
# # admin.site.register(User)
# admin.site.register(User, UserAdmin)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (CarWashRegistrationAdmin,)


admin.site.unregister(Group)
