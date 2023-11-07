from rest_framework.generics import ListAPIView
from carwash.serializers import CarWashServiceSerializer
from carwash.models import CarWashService


class CarWashServiceListAPIView(ListAPIView):
    queryset = CarWashService.objects.all()
    serializer_class = CarWashServiceSerializer

