from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']

    
    def validate_email(self, value):
        users = User.objects.filter(email__iexact=value)
        if self.instance is not None:
            users = users.exclude(pk=self.instance.pk)
        if value and users.exists():
            raise serializers.ValidationError('Этот email уже занят')
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8,
                                     style={'input_type': 'password'})
 
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
 
    def validate_password(self, value):
        password_validation.validate_password(value)
        return value
 
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
 
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Старый пароль указан неверно')
        return value
 
    def validate_new_password(self, value):
        password_validation.validate_password(value, self.context['request'].user)
        return value
 
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])
        return user
