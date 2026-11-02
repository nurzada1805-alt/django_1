from django.contrib import admin
from .models import Note,Category

 
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'is_done', 'created_at','priority')
    list_filter = ('is_done',)
    search_fields = ('title', 'text')


