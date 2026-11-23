from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
 
 
class JWTFlowTests(APITestCase):
 
    def setUp(self):
        cache.clear()
 
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
 
 
class ProfileTests(APITestCase):
 
    @classmethod
    def setUpTestData(cls):
        cls.masha = User.objects.create_user('masha', password='StrongPass123')
 
    def setUp(self):
        cache.clear()
 
    def login(self, password='StrongPass123'):
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'masha', 'password': password,
        }, format='json')
        return response.data
 
    def test_patch_profile(self):
        self.client.force_authenticate(user=self.masha)
        response = self.client.patch(reverse('me'), {
            'email': 'masha@example.com', 'username': 'hacker',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.masha.refresh_from_db()
        self.assertEqual(self.masha.email, 'masha@example.com')
        self.assertEqual(self.masha.username, 'masha')  # read_only — проигнорирован
 
    def test_put_is_not_allowed(self):
        self.client.force_authenticate(user=self.masha)
        response = self.client.put(reverse('me'), {'email': 'a@b.c'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
 
    def test_wrong_old_password(self):
        self.client.force_authenticate(user=self.masha)
        response = self.client.post(reverse('change_password'), {
            'old_password': 'nope', 'new_password': 'NewStrongPass456',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)
 
    def test_change_password_revokes_old_tokens(self):
        old = self.login()


        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {old['access']}")
        response = self.client.post(reverse('change_password'), {
            'old_password': 'StrongPass123', 'new_password': 'NewStrongPass456',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new = response.data
 
        # старый access больше не пускает
        response = self.client.get(reverse('me'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
 
        # новый — пускает
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {new['access']}")
        self.assertEqual(self.client.get(reverse('me')).status_code, status.HTTP_200_OK)
 
        # старый refresh ещё выдаёт access, но этот access тоже не пускает
        self.client.credentials()
        response = self.client.post(reverse('token_refresh'), {'refresh': old['refresh']},
                                    format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        self.assertEqual(self.client.get(reverse('me')).status_code,
                         status.HTTP_401_UNAUTHORIZED)
        self.client.credentials()
 
        # и войти можно уже только с новым паролем
        self.assertNotIn('access', self.login())
        self.assertIn('access', self.login('NewStrongPass456'))
