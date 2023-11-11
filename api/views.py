from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from carwash.serializers import *
from carwash.models import CarWashService
from common.views import carwash_user_registration_delete


class CarWashServiceListAPIView(generics.ListAPIView):
    queryset = CarWashService.objects.all()
    serializer_class = CarWashServiceSerializer


class CarWashRegistrationAPIView(APIView):
    pass


class CarWashUserRegistrationAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_response(request):
        all_user_reg = CarWashUserRegistration.objects.filter(client=request.user)
        return Response({'user_registrations': CarWashUserRegistrationSerializer(all_user_reg, many=True).data})

    def get(self, request):
        return self.get_response(request)

    def delete(self, request, registration_pk):
        carwash_user_registration_delete(request, registration_pk)
        return self.get_response(request)


class CarWashRequestCallCreateAPIView(generics.CreateAPIView):
    serializer_class = CarWashRequestCallSerializer
    permission_classes = (IsAuthenticated,)
