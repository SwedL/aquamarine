from carwash.services.staff_detail_view_service import StaffDetailViewService
from common.utils import prepare_workdays


class StaffDetailViewUseCase:
    staff_detail_view_service = StaffDetailViewService()

    def execute(self, request, days_delta: int) -> dict:
        week_workday_objects = prepare_workdays()
        context = self.staff_detail_view_service.get_context(
            user=request.user,
            days_delta=days_delta,
            week_workday_objects=week_workday_objects,
        )
        return context