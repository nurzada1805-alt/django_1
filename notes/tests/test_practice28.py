from django.urls import reverse
 
from notes.models import Category, Note
 
from .base import NotesAPITestCase
 
 
class StatsByCategoryTests(NotesAPITestCase):
 
    def test_by_category(self):
        home = Category.objects.create(name='Дом', slug='home')
        Note.objects.create(title='Полить цветы', text='утром', is_done=True,
                            author=self.masha, category=home)
        Note.objects.create(title='Чужая', author=self.dima, category=home)
        self.client.force_authenticate(user=self.masha)
        with self.assertNumQueries(2):
            response = self.client.get(reverse('note-stats'))
        self.assertEqual(response.data['by_category'], [
            {'category_name': 'Дом', 'total': 1, 'done': 1},
            {'category_name': 'Работа', 'total': 1, 'done': 0},
        ])
 
    def test_notes_without_category_go_last(self):
        Note.objects.create(title='Без категории', author=self.masha)
        self.client.force_authenticate(user=self.masha)
        response = self.client.get(reverse('note-stats'))
        self.assertEqual(response.data['by_category'][-1],
                         {'category_name': None, 'total': 1, 'done': 0})
