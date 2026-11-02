from django.db import models
from django.contrib.auth.models import User

 
 
class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('Слаг', max_length=100, unique=True)
 
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
 
    def __str__(self):
        return self.name
 
 
class Note(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    text = models.TextField('Текст', blank=True)
    is_done = models.BooleanField('Выполнена', default=False)
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    priority = models.IntegerField(default=1)
 
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='notes',
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='notes',
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
 
    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at']
 
    def __str__(self):
        return self.title