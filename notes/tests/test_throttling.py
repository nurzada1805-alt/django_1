from unittest import mock
 
from django.urls import reverse
from rest_framework import status
 
from notes.throttles import NoteCreateThrottle
 
from .base import NotesAPITestCase
 
 
class LoginThrottleTests(NotesAPITestCase):
 
    def test_sixth_login_attempt_gets_429(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'masha', 'password': 'wrong'}
        for _ in range(5):
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn('Retry-After', response.headers)
 
 
class NoteCreateThrottleTests(NotesAPITestCase):
 
    @mock.patch.object(NoteCreateThrottle, 'THROTTLE_RATES', {'note_create': '2/hour'})
    def test_only_create_is_limited(self):
        self.client.force_authenticate(user=self.masha)
        url = reverse('note-list')
        codes = [self.client.post(url, {'title': f'Заметка {i}'}, format='json').status_code
                 for i in range(3)]
        self.assertEqual(codes, [201, 201, 429])
        # читать список по-прежнему можно: лимит только на create
        self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
 
    @mock.patch.object(NoteCreateThrottle, 'THROTTLE_RATES', {'note_create': '2/hour'})
    def test_limit_is_per_user(self):
        url = reverse('note-list')
        self.client.force_authenticate(user=self.masha)
        for i in range(2):
            self.client.post(url, {'title': f'Маша {i}'}, format='json')
        self.client.force_authenticate(user=self.dima)
        response = self.client.post(url, {'title': 'Дима 1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
