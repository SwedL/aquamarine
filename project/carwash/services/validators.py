from typing import Any

from carwash.exceptions.exceptions import TimeAlreadyTakenException
from carwash.models import CarWashWorkDay

class FreeTimeCarWashWorkDayValidatorService:
    @staticmethod
    def validate(attributes: dict[str, Any]) -> None:
        """Проверяем свободно ли ещё время пока пользователь делал свой выбор"""

        workday = CarWashWorkDay.objects.filter(date=attributes['date']).first()
        process_times = attributes['process_times']
        total_time = attributes['total_time']
        check_free_times = [getattr(workday, 'time_' + process_times.pop(0).replace(':', '')) for _ in
                            range(0, total_time, 30)]
        if any([x for x in check_free_times]):
            raise TimeAlreadyTakenException()