from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
 
from .serializers import RegisterSerializer, UserSerializer
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ChangePasswordSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

 
 
class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_scope = 'register'


class LoginView(TokenObtainPairView):
    """Вход: логин и пароль → access + refresh. Не больше 5 попыток в минуту."""
    throttle_scope = 'auth'
 
 
class MeView(generics.RetrieveUpdateAPIView):
    """Профиль текущего пользователя: посмотреть и поправить."""
    serializer_class = UserSerializer
    http_method_names = ['get', 'patch', 'head', 'options']
 
    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.GenericAPIView):

    """Смена пароля. Старые токены перестают работать — выдаём новые."""
    serializer_class = ChangePasswordSerializer
 
    @extend_schema(responses=inline_serializer(
        name='TokenPair',
        fields={'access': serializers.CharField(), 'refresh': serializers.CharField()},
    ))


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({'access': str(refresh.access_token), 'refresh': str(refresh)})


    def test_change_password_revokes_old_tokens(self):
    # 1. Получаем начальную пару токенов (логин)
        response = self.client.post('/api/auth/token/', {
            'username': 'testuser',
            'password': 'oldpassword123'
        })
        refresh_token = response.data['refresh']

    # 2. Меняем пароль
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
        response = self.client.post('/api/auth/password/', {
            'old_password': 'oldpassword123',
            'new_password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 3. Пытаемся обновить access-токен с помощью СТАРОГО refresh-токена
        refresh_response = self.client.post('/api/auth/token/refresh/', {
            'refresh': refresh_token
        })
    
    # ИСПРАВЛЕНИЕ: теперь старый токен в блеклисте, поэтому ожидаем 401 Unauthorized
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)



