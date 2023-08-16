from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *


@admin.register(CarWashService)
class CarWashServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'process_time', 'price_standart', 'price_crossover', 'price_offroad')
    list_display_links = ('name',)


# @admin.register(CarWashRegistration)
# class CarWashRegistrationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'client')
#     list_filter = ('client',)
#     filter_horizontal = ('services',)
#     ordering = ('id',)

class CarWashRegistrationAdmin(admin.TabularInline):
    model = CarWashRegistration
    fields = ('id', 'client', )
    # readonly_fields = ('created_timestamp',)
    extra = 0


@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    list_display = ('date',)
    search_fields = ('date',)
    ordering = ('-date',)
