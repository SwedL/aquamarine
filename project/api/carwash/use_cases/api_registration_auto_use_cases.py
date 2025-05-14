from api.carwash.services.api_registration_auto_get_services import \
    APIRegistrationAutoGetService
from api.carwash.services.api_registration_auto_post_services import \
    APIRegistrationAutoPostService
from carwash.serializers import RegistrationSerializer
from common.utils import prepare_workdays
from rest_framework.request import Request


class APIRegistrationAutoGetUseCase:
    api_registration_auto_get_service = APIRegistrationAutoGetService()

    def execute(self) -> dict:
        # проверяем наличие объектов CarWashWorkDay на неделю вперёд и получаем их из функции
        week_workday_objects = prepare_workdays()
        context = self.api_registration_auto_get_service.get_context(
            week_workday_objects=week_workday_objects,
        )
        return context


class APIRegistrationAutoPostUseCase:
    api_registration_auto_post_service = APIRegistrationAutoPostService()
    registration_serializer = RegistrationSerializer

    def execute(self, request: Request) -> dict:
        # проверяем наличие объектов CarWashWorkDay на неделю вперёд
        prepare_workdays()
        serializer = self.registration_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        context = self.api_registration_auto_post_service.create_registration(request=request)

        return context
