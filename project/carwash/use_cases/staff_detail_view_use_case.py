from django.core.handlers.asgi import ASGIRequest

from carwash.services.staff_detail_view_service import StaffDetailViewService
from common.utils import prepare_workdays, delete_old_record


class StaffDetailViewUseCase:
    staff_detail_view_service = StaffDetailViewService()

    def execute(self, request: ASGIRequest, days_delta: int) -> dict:
        week_workday_objects = prepare_workdays()
        delete_old_record()  # удаляем старые записи, старше 1 года
        context = self.staff_detail_view_service.get_context(
            user=request.user,
            days_delta=days_delta,
            week_workday_objects=week_workday_objects,
        )
        return context