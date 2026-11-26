from rest_framework import serializers
 
from .models import Category, Note
 
MAX_ATTACHMENT_SIZE = 2 * 1024 * 1024  # 2 МБ
 
 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
 
 
class CategoryWithCountSerializer(CategorySerializer):
    """Категория + сколько в ней заметок текущего пользователя."""
    notes_count = serializers.IntegerField(read_only=True)
 
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['notes_count']
 
 
class NoteSerializer(serializers.ModelSerializer):
    """Читаем связь вложенным объектом, пишем по id."""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True,
    )
    author = serializers.CharField(source='author.username', read_only=True, allow_null=True)
    status = serializers.SerializerMethodField()
 
    class Meta:
        model = Note
        fields = ['id', 'title', 'text', 'status', 'is_done',
                  'category', 'category_id', 'author', 'attachment', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'title': {'error_messages': {'required': 'Введите заголовок'}},
        }
 
    def get_status(self, obj) -> str:
        return 'выполнена' if obj.is_done else 'в работе'
 
    def validate_title(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError('Минимум 3 символа')
        if value.isdigit():
            raise serializers.ValidationError('Заголовок не может быть числом')
        return value
 
    def validate_attachment(self, value):
        if value and value.size > MAX_ATTACHMENT_SIZE:
            raise serializers.ValidationError('Файл больше 2 МБ')
        return value
 
    def validate(self, attrs):
        is_done = attrs.get('is_done', getattr(self.instance, 'is_done', False))
        text = attrs.get('text', getattr(self.instance, 'text', ''))
        if is_done and not text:
            raise serializers.ValidationError(
                {'text': 'Нельзя закрыть заметку без описания'}
            )
        return attrs


