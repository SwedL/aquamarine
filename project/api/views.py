from datetime import date

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.carwash.use_cases.api_registration_auto_use_cases import (
    APIRegistrationAutoGetUseCase, APIRegistrationAutoPostUseCase)
from carwash.models import CarWashRegistration, CarWashService
from carwash.serializers import (CarWashRegistrationSerializer,
                                 CarWashRequestCallSerializer,
                                 CarWashServiceSerializer)
from carwash.services.user_registration_cancel_service import \
    user_registration_cancel
from carwash.views import RegistrationAutoView
from users.models import User
from users.serializers import UserSerializer


class CarWashServiceListAPIView(generics.ListAPIView):
    """ Представление для получения списка доступных услуг компании. """
    queryset = CarWashService.objects.all()
    serializer_class = CarWashServiceSerializer


class CarWashRegistrationAPIView(RegistrationAutoView, APIView):
    permission_classes = (IsAuthenticated,)
    api_registration_auto_get_use_cases = APIRegistrationAutoGetUseCase()
    api_registration_auto_post_use_cases = APIRegistrationAutoPostUseCase()

    @swagger_auto_schema(operation_description='Получение списка всех услуг компании, \n'
                                               'а также информации доступных дней и времени.')
    def get(self, request):
        context = self.api_registration_auto_get_use_cases.execute()
        return Response(context)

    @swagger_auto_schema(method='post',
                         operation_description='Запись автомобиля на выбранные дату, время и id услуг \n'
                                               '"selected_date_and_time" формат "YYYY MM DD,HH:MM"\n'
                                               '"services_ids" формат "1 2 3"',
                         request_body=openapi.Schema(properties={
                             'selected_date_and_time': openapi.Schema(type=openapi.TYPE_STRING,
                                                                      pattern=r'2\d{3}\s\d\d\s\d\d,\d\d:\d\d'),
                             'services_ids': openapi.Schema(type=openapi.TYPE_STRING,
                                                            pattern=r'[\d{1,2}\s]{1,17}'),
                         },
                             type=openapi.TYPE_OBJECT)
                         )
    @action(methods=['post'], detail=False)
    def post(self, request: Request, *args, **kwargs):
        context = self.api_registration_auto_post_use_cases.execute(request=request)
        return Response(context)


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
        user_registration_cancel(request, kwargs['pk'])
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
