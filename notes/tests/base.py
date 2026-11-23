from django.contrib.auth.models import User
from rest_framework.test import APITestCase
 
from notes.models import Category, Note
from django.core.cache import cache
 
 
class NotesAPITestCase(APITestCase):
    """Общая подготовка: три пользователя, категория и две заметки."""
 
    @classmethod
    def setUpTestData(cls):
        cls.masha = User.objects.create_user('masha', password='StrongPass123')
        cls.dima = User.objects.create_user('dima', password='StrongPass123')
        cls.admin = User.objects.create_user('admin', password='StrongPass123',
                                             is_staff=True)
        cls.work = Category.objects.create(name='Работа', slug='work')
        cls.masha_note = Note.objects.create(title='Купить хлеб', author=cls.masha,
                                             category=cls.work)
        cls.dima_note = Note.objects.create(title='Позвонить маме', author=cls.dima)


    def setUp(self):
        # Счётчики троттлинга живут в кеше и переживают тест — обнуляем
        cache.clear()
