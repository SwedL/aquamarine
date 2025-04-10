from django.core.handlers.asgi import ASGIRequest

from carwash.services.registration_auto_get_services import RegistrationAutoGetService
from carwash.services.registration_auto_post_services import RegistrationAutoPostService
from common.utils import prepare_workdays


class RegistrationAutoGetUseCase:
    registration_auto_get_service = RegistrationAutoGetService()

    def execute(self, request: ASGIRequest) -> tuple[str, dict]:
        # проверяем наличие объектов CarWashWorkDay на неделю вперёд и получаем их из функции
        week_workday_objects = prepare_workdays()
        template_name, context = self.registration_auto_get_service.get_context(
            user=request.user,
            week_workday_objects=week_workday_objects,
        )
        return template_name, context


class RegistrationAutoPostUseCase:
    registration_auto_post_service = RegistrationAutoPostService()

    def execute(self, request: ASGIRequest) -> tuple[str, dict]:
        prepare_workdays()
        template_name, context = self.registration_auto_post_service.create_registration(request=request)
        return template_name, context
