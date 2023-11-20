from rest_framework import serializers
from carwash.models import *


class CarWashServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWashService
        fields = ('id', 'name', 'process_time', 'price_standart', 'price_crossover', 'price_offroad')


class CarWashRegistrationSerializer(serializers.ModelSerializer):
    services = serializers.StringRelatedField(many=True)

    class Meta:
        model = CarWashRegistration
        fields = ('id', 'client', 'services', 'date_reg', 'time_reg', 'total_time', 'total_cost', 'relation_carwashworkday')
        ordering = ('date_reg', 'time_reg')


class CarWashWorkDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWashWorkDay
        fields = '__all__'


class CarWashRequestCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWashRequestCall
        fields = ('phone_number',)
