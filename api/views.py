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
    serializer_class = CarWashUserRegistrationSerializer
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_list_services(request):
        result_lst = CarWashUserRegistration.objects.filter(client=request.user).values()
        for i in result_lst:
            i['carwash_reg_id'] = CarWashRegistration.objects.filter(id=i['carwash_reg_id'])[0].__str__()
        return sorted(result_lst, key=lambda x: (x['date_reg'], x['time_reg']))

    def get(self, request):
        return Response({'user_registration': list(self.get_list_services(request))})

    def post(self, request, registration_pk):
        carwash_user_registration_delete(request, registration_pk)
        return Response({'user_registration': list(self.get_list_services(request))})


class CarWashRequestCallCreateAPIView(generics.CreateAPIView):
    serializer_class = CarWashRequestCallSerializer
    permission_classes = (IsAuthenticated,)
