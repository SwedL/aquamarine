from django.core.handlers.asgi import ASGIRequest

from api.carwash.services.api_registration_auto_get_services import APIRegistrationAutoGetService
from carwash.services.registration_auto_get_services import CreateWeekWorkdayService
from carwash.services.registration_auto_post_services import RegistrationAutoPostService


class APIRegistrationAutoGetUseCase:
    create_week_workday_service = CreateWeekWorkdayService
    api_registration_auto_get_service = APIRegistrationAutoGetService()

    def execute(self) -> dict:
        # проверяем наличие объектов CarWashWorkDay на неделю вперёд и получаем их из функции
        week_workday_objects = self.create_week_workday_service.prepare_workdays()
        context = self.api_registration_auto_get_service.get_context(
            week_workday_objects=week_workday_objects,
        )
        return context


class RegistrationAutoPostUseCase:
    registration_auto_post_service = RegistrationAutoPostService()

    def execute(self, request: ASGIRequest) -> dict:
        context = self.registration_auto_post_service.get_context()

        return context
