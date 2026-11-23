from unittest import mock
from django.urls import reverse
from rest_framework.test import APITestCase


class HealthTests(APITestCase):

    
    def test_healthy(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'database': 'ok', 'cache': 'ok'})


    def test_cache_down_gives_503(self):
        with mock.patch('config.views.cache.set', side_effect=ConnectionError):
            response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()['cache'], 'error')