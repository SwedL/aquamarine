from rest_framework import serializers
from carwash.models import CarWashService


class CarWashServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWashService
        fields = ['id', 'name', 'process_time', 'price_standart', 'price_crossover', 'price_offroad']
