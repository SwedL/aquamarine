from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from carwash.serializers import *
from carwash.models import CarWashService


class CarWashServiceListAPIView(generics.ListAPIView):
    queryset = CarWashService.objects.all()
    serializer_class = CarWashServiceSerializer


class CarWashRequestCallCreateAPIView(generics.CreateAPIView):
    serializer_class = CarWashRequestCallSerializer
    permission_classes = (IsAuthenticated,)


class CarWashUserRegistrationListAPIView(mixins.ListModelMixin,
                                         mixins.DestroyModelMixin,
                                         GenericViewSet):
    queryset = CarWashUserRegistration.objects.all()
    serializer_class = CarWashUserRegistrationSerializer

    def get_queryset(self):
        queryset = super(CarWashUserRegistrationListAPIView, self).get_queryset()
        return queryset.filter(date_reg__gte=date.today(), client=self.request.user)

