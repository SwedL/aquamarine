from django.contrib import admin

from carwash.models import (CarWashRegistration, CarWashRequestCall,
                            CarWashService, CarWashWorkDay)


@admin.register(CarWashService)
class CarWashServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'process_time', 'price_standart', 'price_crossover', 'price_offroad')
    list_display_links = ('name',)


# class CarWashRegistrationAdmin(admin.StackedInline):
#     model = CarWashRegistration
#     fields = ('id', 'client')
#     extra = 0
#
#     def has_delete_permission(self, request, obj=None):
#         # Disable delete
#         return False
#
#     def has_add_permission(self, request, obj=None):
#         # Disable add
#         return False


@admin.register(CarWashWorkDay)
class CarWashWorkDayAdmin(admin.ModelAdmin):

    readonly_fields = ('date',)
    list_display = ('date', 'pk',)
    search_fields = ('date',)
    ordering = ('-date',)


@admin.register(CarWashRegistration)
class CarWashRegistrationAdmin(admin.ModelAdmin):

    list_display = ('id', 'client', 'date_reg', 'time_reg')
    fields = ('client', ('date_reg', 'time_reg',), 'relation_carwashworkday')
    readonly_fields = ('client', 'date_reg', 'time_reg')
    ordering = ('-date_reg', '-time_reg',)


@admin.register(CarWashRequestCall)
class CarWashCallMeAdmin(admin.ModelAdmin):

    list_display = ('phone_number', 'processed', 'created',)
    ordering = ('-created',)
