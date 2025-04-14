from carwash.models import CarWashRegistration, CarWashWorkDay


def staff_registration_cancel(registration_id: int) -> None:
    """Функция для StaffCancelRegistrationView - 'отмены (удаления)'
     сотрудником записи клиента."""
    registration_auto = CarWashRegistration.objects.filter(id=registration_id).first()
    workday = CarWashWorkDay.objects.get(date=registration_auto.date_reg)
    time_attributes = registration_auto.relation_carwashworkday['time_attributes']

    # удаляем записи выбранной CarWashRegistration в полях времени CarWashWorkDay,
    # значению поля соответствующего времени присваиваем значение None (как по умолчанию)
    [setattr(workday, time_attribute, None) for time_attribute in time_attributes]
    workday.save()
