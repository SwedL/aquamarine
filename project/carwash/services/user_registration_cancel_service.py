from carwash.models import CarWashRegistration, CarWashWorkDay
from django.http import Http404


def user_registration_cancel(request, registration_pk):
    """Функция для UserRegistrationsCancelView и UserRegistrationListAPIView - обработчик
     события 'отмены (удаления)' пользователем своей записи на автомоечный комплекс."""
    user_registration = CarWashRegistration.objects.filter(pk=registration_pk).first()

    # проверка, что пользователь удаляет принадлежащую ему CarWashUserRegistration
    if not user_registration or user_registration.client != request.user:
        raise Http404

    need_workday = CarWashWorkDay.objects.get(date=user_registration.date_reg)
    time_attributes = user_registration.relation_carwashworkday['time_attributes']
    [setattr(need_workday, t_a, None) for t_a in time_attributes]
    need_workday.save()
    user_registration.delete()
