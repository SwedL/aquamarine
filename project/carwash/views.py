from datetime import date

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.views import View
from django.views.generic import FormView, ListView

from carwash.forms import CarWashRequestCallForm
from carwash.models import (CarWashRegistration, CarWashRequestCall,
                            CarWashService, CarWashWorkDay)
from carwash.use_cases.staff_detail_view_use_case import StaffDetailViewUseCase
from common.utils import Common

from carwash.services.user_registration_cancel_service import user_registration_cancel
from carwash.use_cases.registration_auto_use_cases import RegistrationAutoGetUseCase, RegistrationAutoPostUseCase
from users.permissions import staff_permission


class IndexListView(Common, ListView):
    """
    Представление для показа главной страницы компании
    и прейскуранта на оказание услуг автомоечного комплекса
    """

    template_name = 'carwash/index.html'
    model = CarWashService
    context_object_name = 'services'
    title = 'Aquamarine'
    # menu_tabs = (1, 2, 3)


class RegistrationAutoView(View):
    """
    Представление пользователю выбора услуг автомоечного комплекса, дня и времени,
     для оказания выбранных услуг.
    Авторизованный пользователь имеет возможность самостоятельной записи автомобиля,
     а неавторизованный пользователя возможность запросить звонок администратора для записи автомобиля
    """
    registration_auto_get_use_case = RegistrationAutoGetUseCase()
    registration_auto_post_use_case = RegistrationAutoPostUseCase()

    def get(self, request):
        template_name, context = self.registration_auto_get_use_case.execute(request=request)

        return render(request, template_name=template_name, context=context)

    def post(self, request):
        template_name, context = self.registration_auto_post_use_case.execute(request=request)

        return render(request, template_name=template_name, context=context)


class UserRegistrationsListView(LoginRequiredMixin, Common, ListView):
    """
    Представление для показа пользователю его записей
     на оказание услуг автомоечного комплекса
    """

    model = CarWashRegistration
    template_name = 'carwash/user-registrations.html'
    context_object_name = 'user_registrations'
    title = 'Мои записи'
    menu_tabs = (0, 1)

    def get_queryset(self):
        queryset = super(UserRegistrationsListView, self).get_queryset()

        return queryset.filter(date_reg__gte=date.today(), client=self.request.user).order_by('date_reg', 'time_reg')


class UserRegistrationsCancelView(LoginRequiredMixin, Common, View):
    """Обработчик события 'отмены (удаления)' пользователем своей записи"""

    def get(self, request, registration_pk):
        user_registration_cancel(request, registration_pk)
        redirect_url = reverse('carwash:user_registrations')

        return HttpResponseRedirect(redirect_url)


class StaffDetailView(Common, PermissionRequiredMixin, View):
    """
    Представление для показа сотруднику всех записей клиентов.
    На сегодня, завтра и послезавтра.
    """

    title = 'Менеджер'
    permission_required = staff_permission
    staff_detail_view_use_case = StaffDetailViewUseCase()
    template_name = 'carwash/staff.html'

    def get(self, request, days_delta: int=0):
        context = self.staff_detail_view_use_case.execute(request=request, days_delta=days_delta)
        context.update({'title': self.title})

        return render(request, template_name=self.template_name, context=context)


class StaffCancelRegistrationView(Common, PermissionRequiredMixin, View):
    """Обработчик события 'отмена (удаление)' сотрудником записи клиента"""

    permission_required = staff_permission

    def get(self, request, days_delta, registration_id):
        need_carwash_registration = CarWashRegistration.objects.filter(id=registration_id).first()
        need_workday = CarWashWorkDay.objects.get(date=need_carwash_registration.date_reg)
        time_attributes = need_carwash_registration.relation_carwashworkday['time_attributes']

        # удаляем записи выбранной CarWashRegistration в полях времени CarWashWorkDay,
        # значению поля соответствующего времени присваиваем значение None (как по умолчанию)
        [setattr(need_workday, t_a, None) for t_a in time_attributes]
        need_workday.save()

        redirect_url = reverse('carwash:staff', kwargs={'days_delta': days_delta})

        return HttpResponseRedirect(redirect_url)


class RequestCallFormView(Common, FormView):
    """Представление для заказа звонка клиенту"""

    form_class = CarWashRequestCallForm
    template_name = 'carwash/request-call.html'
    title = 'Заказ звонка'
    menu_tabs = (0, 1)

    def form_valid(self, form):
        call_me = CarWashRequestCall(phone_number=form.cleaned_data['phone_number'])
        call_me.save()

        context = {
            'title': self.title,
            'menu': self.create_menu((0, 1)),
            'staff': self.request.user.is_staff,
        }

        return render(self.request, 'carwash/request-call-done.html', context=context)


class RequestCallProcessingView(View):
    """Обработчик события 'обработка звонка'"""

    permission_required = staff_permission

    def get(self, request, days_delta, call_pk):
        processed_call = CarWashRequestCall.objects.get(pk=call_pk)
        processed_call.processed = True
        processed_call.save()
        redirect_url = reverse('carwash:staff', kwargs={'days_delta': days_delta})

        return HttpResponseRedirect(redirect_url)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
