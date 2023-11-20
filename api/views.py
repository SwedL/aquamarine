from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from carwash.serializers import *
from carwash.models import CarWashService
from carwash.views import RegistrationAutoView
from common.views import carwash_user_registration_delete, create_and_get_week_workday
from users.serializers import UserSerializer


class CarWashServiceListAPIView(generics.ListAPIView):
    queryset = CarWashService.objects.all()
    serializer_class = CarWashServiceSerializer


class CarWashRegistrationAPIView(RegistrationAutoView, APIView):
    def get(self, request):
        c = CarWashService.objects.all()
        w = create_and_get_week_workday()
        return Response({'services': CarWashServiceSerializer(c, many=True).data,
                         'wordays_week': CarWashWorkDaySerializer(w, many=True).data})

    def post(self, request):
        context = super(CarWashRegistrationAPIView, self).post(request)

        if context['title'] == 'Ошибка записи':
            return Response({'title': 'Ошибка записи',
                             'message': 'Время которые вы выбрали уже занято. Попробуйте выбрать другое время'})

        return Response({'title': 'Запись зарегистрирована',
                         'choice_services': CarWashServiceSerializer(context['choice_services'], many=True).data,
                         'normal_format_choicen_date': context['normal_format_choicen_date'],
                         'choice_time': context['choice_time'],
                         'total_time': context['total_time'],
                         'total_cost': context['total_cost'],
                         })


class UserRegistrationListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_response(request):
        all_user_reg = CarWashRegistration.objects.filter(date_reg__gte=date.today(), client=request.user)
        return Response({'user_registrations': CarWashRegistrationSerializer(all_user_reg, many=True).data})

    def get(self, request):
        return self.get_response(request)

    def delete(self, request, registration_pk):
        carwash_user_registration_delete(request, registration_pk)
        return self.get_response(request)


class CarWashRequestCallCreateAPIView(generics.CreateAPIView):
    serializer_class = CarWashRequestCallSerializer
    permission_classes = (IsAuthenticated,)


class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

