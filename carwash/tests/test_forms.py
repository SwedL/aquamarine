from django.test import TestCase
from carwash.forms import CarWashRequestCallForm


class RequestCallFormViewTestCase(TestCase):

    def setUp(self):
        self.form = CarWashRequestCallForm()

    def test_form_field_label(self):
        # Проверка названий полей формы
        self.assertTrue(
            self.form.fields['phone_number'].label is None or
            self.form.fields['phone_number'].label == 'phone_number'
        )
        self.assertTrue(
            self.form.fields['captcha'].label is None or
            self.form.fields['captcha'].label == 'captcha'
        )

    def test_form_phone_number_help_message(self):
        # Проверка вспомогательного сообщения формы
        self.assertEqual(
            self.form.fields['phone_number'].validators[0].message,
            "Номер телефона должен быть в формате: '89999999999'"
        )
