from rest_framework import serializers

from .models import (CarWashRegistration, CarWashRequestCall, CarWashService,
                     CarWashWorkDay)


class CarWashServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWashService
        fields = ('id', 'name', 'process_time', 'price_standart', 'price_crossover', 'price_offroad')


class RegistrationSerializer(serializers.Serializer):
    regex = r'2\d{3}\s\d\d\s\d\d,\d\d:\d\d'
    selected_date_and_time = serializers.RegexField(regex, max_length=16, min_length=16)
    services_ids = serializers.ListField(child=serializers.IntegerField(min_value=0, max_value=100), allow_empty=False)

    def is_valid(self, *, raise_exception=False):
        super().is_valid()
        return not bool(self.errors)


class CarWashRegistrationSerializer(serializers.ModelSerializer):
    services = serializers.StringRelatedField(many=True)

    class Meta:
        model = CarWashRegistration
        fields = (
            'id',
            'client',
            'services',
            'date_reg',
            'time_reg',
            'total_time',
            'total_cost',
            'relation_carwashworkday',
        )
        ordering = ('date_reg', 'time_reg')


class CarWashWorkDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWashWorkDay
        fields = '__all__'


class CarWashRequestCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWashRequestCall
        fields = ('phone_number',)
