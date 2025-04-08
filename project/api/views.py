from datetime import date

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from carwash.models import CarWashRegistration, CarWashService
from carwash.serializers import (CarWashRegistrationSerializer,
                             CarWashRequestCallSerializer,
                             CarWashServiceSerializer,
                             CarWashWorkDaySerializer,
                             RegistrationSerializer)
from carwash.views import RegistrationAutoView
from common.views import (carwash_user_registration_delete,
                          create_and_get_week_workday)
from users.models import User
from users.serializers import UserSerializer


class CarWashServiceListAPIView(generics.ListAPIView):
    """ Представление для получения списка доступных услуг компании. """
    queryset = CarWashService.objects.all()
    serializer_class = CarWashServiceSerializer


class CarWashRegistrationAPIView(RegistrationAutoView, APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_description='Получение списка всех услуг компании, \n'
                                               'а также информации доступных дней и времени.')
    def get(self, request):
        c = CarWashService.objects.all()
        w = create_and_get_week_workday()
        return Response({'services': CarWashServiceSerializer(c, many=True).data,
                         'workdays_week': CarWashWorkDaySerializer(w, many=True).data})

    @swagger_auto_schema(method='post',
                         operation_description='Запись автомобиля на выбранные дату, время и id услуг \n'
                                               '"choice_date_and_time" формат "YYYY MM DD,HH:MM"\n'
                                               '"services_list" формат "1 2 3"',
                         request_body=openapi.Schema(properties={
                             'choice_date_and_time': openapi.Schema(type=openapi.TYPE_STRING,
                                                                    pattern=r'2\d{3}\s\d\d\s\d\d,\d\d:\d\d'),
                             'services_list': openapi.Schema(type=openapi.TYPE_STRING,
                                                             pattern=r'[\d{1,2}\s]{1,17}'),
                         },
                             type=openapi.TYPE_OBJECT)
                         )
    @action(methods=['post'], detail=False)
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.data['services_list'] = list(map(int, request.data['services_list'].split()))

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


class UserRegistrationListAPIView(mixins.DestroyModelMixin,
                                  mixins.ListModelMixin,
                                  GenericViewSet):
    """
    Представление получения всех записей пользователя на автомойку.
    Удаление записи пользователя на автомойку по id записи.
    """

    serializer_class = CarWashRegistrationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = CarWashRegistration.objects.filter(date_reg__gte=date.today(), client=self.request.user)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        carwash_user_registration_delete(request, kwargs['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CarWashRequestCallCreateAPIView(generics.CreateAPIView):
    """ Представление для запроса звонка пользователю """

    serializer_class = CarWashRequestCallSerializer
    permission_classes = (IsAuthenticated,)


class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    """ Представление получения и изменения данных пользователя """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
