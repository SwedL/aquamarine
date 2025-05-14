from carwash.models import (CarWashRegistration, CarWashRequestCall,
                            CarWashService, CarWashWorkDay)
from django.contrib import admin


@admin.register(CarWashService)
class CarWashServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'process_time', 'price_standart', 'price_crossover', 'price_offroad')
    list_display_links = ('name',)


@admin.register(CarWashWorkDay)
class CarWashWorkDayAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
    list_display = ('date', 'pk')
    search_fields = ('date',)
    ordering = ('-date',)


@admin.register(CarWashRegistration)
class CarWashRegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date_reg', 'time_reg')
    fields = (('date_reg', 'time_reg',), 'services', 'relation_carwashworkday')
    readonly_fields = ('client', 'date_reg', 'time_reg', 'services')
    list_display_links = ('client',)
    ordering = ('-date_reg', '-time_reg',)


@admin.register(CarWashRequestCall)
class CarWashCallMeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'processed', 'created')
    ordering = ('-created',)


admin.site.site_title = 'Администрирование Aquamarine company'
admin.site.site_header = 'Администрирование Aquamarine company'
