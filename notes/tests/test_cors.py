from django.urls import reverse
from rest_framework.test import APITestCase
 
 
class CorsTests(APITestCase):
 
    def preflight(self, origin):
        return self.client.options(
            reverse('note-list'),
            HTTP_ORIGIN=origin,
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='GET',
            HTTP_ACCESS_CONTROL_REQUEST_HEADERS='authorization',
        )
 
    def test_allowed_origin(self):
        response = self.preflight('http://localhost:5173')
        self.assertEqual(response.headers['Access-Control-Allow-Origin'],
                         'http://localhost:5173')
        self.assertIn('authorization', response.headers['Access-Control-Allow-Headers'])
 
    def test_unknown_origin(self):
        response = self.preflight('http://evil.example')
        self.assertNotIn('Access-Control-Allow-Origin', response.headers)
