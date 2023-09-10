from django.contrib import admin
from django import forms
from .models import *


@admin.register(CarWashService)
class CarWashServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'process_time', 'price_standart', 'price_crossover', 'price_offroad')
    list_display_links = ('name',)


class CarWashRegistrationAdmin(admin.StackedInline):
    model = CarWashRegistration
    fields = ('id', 'client', )
    extra = 0

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False

    def has_add_permission(self, request, obj=None):
        # Disable add
        return False


@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):

    readonly_fields = ('date',)
    list_display = ('date', 'pk')
    search_fields = ('date',)
    ordering = ('-date',)


@admin.register(CarWashUserRegistration)
class CarWashUserRegistrationAdmin(admin.ModelAdmin):

    list_display = ('date_reg', 'time_reg', 'client')
    ordering = ('-date_reg', '-time_reg')

# admin.site.register(CarWashUserRegistration)