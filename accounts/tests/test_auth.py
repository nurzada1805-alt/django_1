from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
 
 
class JWTFlowTests(APITestCase):
 
    def test_full_cycle(self):
        # 1. Регистрация
        response = self.client.post(reverse('register'), {
            'username': 'lena', 'email': 'lena@example.com', 'password': 'StrongPass123',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)
        self.assertTrue(User.objects.get(username='lena').check_password('StrongPass123'))
 
        # 2. Вход
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'lena', 'password': 'StrongPass123',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access, refresh = response.data['access'], response.data['refresh']
 
        # 3. Запрос с токеном
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.get(reverse('me'))
        self.assertEqual(response.data['username'], 'lena')
 
        # 4. Обновление: при ротации приходит и новый refresh
        response = self.client.post(reverse('token_refresh'), {'refresh': refresh},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_refresh = response.data['refresh']
 
        # 5. Старый refresh уже в чёрном списке
        response = self.client.post(reverse('token_refresh'), {'refresh': refresh},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
 
        # 6. Выход и попытка обновиться
        response = self.client.post(reverse('token_blacklist'), {'refresh': new_refresh},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(reverse('token_refresh'), {'refresh': new_refresh},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
 
    def test_wrong_password(self):
        User.objects.create_user('lena', password='StrongPass123')
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'lena', 'password': 'wrong',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
 
    def test_weak_password_is_rejected(self):
        response = self.client.post(reverse('register'), {
            'username': 'lena', 'password': '12345678',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
