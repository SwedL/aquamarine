from django.contrib import admin
from .models import *


@admin.register(CarWashService)
class CarWashServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'process_time', 'price_standart', 'price_crossover', 'price_offroad')
    list_display_links = ('name',)


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
