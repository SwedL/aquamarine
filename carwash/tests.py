from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from carwash.models import CarWashService
from users.models import User


class TestIndexListView(TestCase):
    def test_view(self):
        path = ''
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Aquamarine')
        self.assertTemplateUsed(response, 'carwash/index.html')



