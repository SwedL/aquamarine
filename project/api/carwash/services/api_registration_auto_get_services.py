from django.db.models import QuerySet

from carwash.models import CarWashService
from carwash.serializers import CarWashServiceSerializer, CarWashWorkDaySerializer


class APIRegistrationAutoGetService:
    def get_context(self, week_workday_objects: QuerySet) -> dict:
        all_service = CarWashService.objects.all()
        context = {
            'services': CarWashServiceSerializer(all_service, many=True).data,
            'workdays_week': CarWashWorkDaySerializer(week_workday_objects, many=True).data
        }
        return context
