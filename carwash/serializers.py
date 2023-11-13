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
        fields = ('id', 'services', 'total_time')


class WorkDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDay
        fields = '__all__'


class CarWashUserRegistrationSerializer(serializers.ModelSerializer):
    carwash_reg = CarWashRegistrationSerializer()

    class Meta:
        model = CarWashUserRegistration
        fields = ('id', 'client', 'date_reg', 'time_reg', 'carwash_reg')
        ordering = ('date_reg', 'time_reg')


class CarWashRequestCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWashRequestCall
        fields = ('phone_number',)

