from django.core.handlers.asgi import ASGIRequest

from carwash.models import CarWashRegistration, CarWashWorkDay, CarWashService
from users.models import User
from carwash.services.registration_auto_get_services import CreateWeekWorkdayService, RegistrationAutoGetService
# from carwash.services.registration_auto_post_services import RegistrationAutoPostService


class RegistrationAutoGetUseCase:
    create_week_workday_service = CreateWeekWorkdayService
    registration_auto_get_service = RegistrationAutoGetService()

    def execute(self, request: ASGIRequest) -> dict:
        # проверяем наличие объектов CarWashWorkDay на неделю вперёд и получаем их из функции
        week_workday_objects = self.create_week_workday_service.prepare_workdays()
        context = self.registration_auto_get_service.get_context(
            user=request.user,
            week_workday_objects=week_workday_objects,
        )
        return context


# class RegistrationAutoPostUseCase:
#     registration_auto_post_service = RegistrationAutoPostService()
#
#     def execute(self, request: ASGIRequest) -> dict:
#         context = self.registration_auto_post_service.get_context()
#
#         return context
