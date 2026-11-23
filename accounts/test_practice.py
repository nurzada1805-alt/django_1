from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
 
 
class EmailUniqueTests(APITestCase):
 
    @classmethod
    def setUpTestData(cls):
        cls.masha = User.objects.create_user('masha', email='masha@example.com',
                                             password='StrongPass123')
        User.objects.create_user('dima', email='dima@example.com', password='StrongPass123')
 
    def setUp(self):
        cache.clear()
        self.client.force_authenticate(user=self.masha)
 
    def test_cannot_take_foreign_email(self):
        response = self.client.patch(reverse('me'), {'email': 'DIMA@example.com'},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'Этот email уже занят')
 
    def test_can_keep_own_email(self):
        response = self.client.patch(reverse('me'), {'email': 'masha@example.com'},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
    def test_can_clear_email(self):
        response = self.client.patch(reverse('me'), {'email': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RegisterThrottleTests(APITestCase):
 
    def setUp(self):
        cache.clear()
 
    def test_fourth_registration_per_hour_is_blocked(self):
        url = reverse('register')
        for i in range(3):
            response = self.client.post(url, {'username': f'user{i}',
                                              'password': 'StrongPass123'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, {'username': 'user4',
                                          'password': 'StrongPass123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
 
    def test_login_has_its_own_limit(self):
        url = reverse('register')
        for i in range(3):
            self.client.post(url, {'username': f'user{i}', 'password': 'StrongPass123'},
                             format='json')
        for _ in range(5):  # все пять попыток входа доступны
            response = self.client.post(reverse('token_obtain_pair'), {
                'username': 'user0', 'password': 'StrongPass123'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
