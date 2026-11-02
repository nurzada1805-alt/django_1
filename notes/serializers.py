from rest_framework import serializers
from .models import Note,Category
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
 
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
 
 
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

 
 
class NoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    text = serializers.CharField(required=False, allow_blank=True)
    is_done = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
    priority = serializers.IntegerField(default=1)


    def create(self, validated_data):
        """Вызывается из save(), когда объекта ещё нет."""
        return Note.objects.create(**validated_data)
 
    def update(self, instance, validated_data):
        """Вызывается из save(), когда объект передан первым аргументом."""
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.is_done = validated_data.get('is_done', instance.is_done)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
    
 
    
class NoteSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    status=serializers.SerializerMethodField()
  

    class Meta:
        model=Note
        fields=['id', 'title','category','author', 'text', 'is_done', 'created_at','priority','status']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
    'title': {
        'error_messages': {
            'required': 'Без заголовка никак',        # ключа нет
            'blank': 'Заголовок не может быть пустым',  # ключ есть, значение ''
        },
        'help_text': 'Коротко: о чём заметка',
    },
    'text': {'required': True},
}
        
    def get_status(self, obj) -> str:
        return 'выполнена' if obj.is_done else 'в работе'

