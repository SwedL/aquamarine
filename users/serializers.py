from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'fio', 'phone_number', 'car_type', 'car_model')
        read_only_fields = ('email', 'car_type')
