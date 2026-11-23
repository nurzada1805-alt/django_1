from rest_framework import status
from rest_framework.reverse import reverse
from notes.models import Note
from .base import NotesAPITestCase


 
class ActiveAndStatsTests(NotesAPITestCase):
 
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Note.objects.create(title='Отчёт', text='готов', is_done=True, author=cls.masha)
        Note.objects.create(title='Купить молоко', author=cls.masha)
 
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.masha)
 
    def test_active_returns_only_not_done(self):
        response = self.client.get(reverse('note-active'))
        titles = sorted(note['title'] for note in response.data['results'])
        self.assertEqual(titles, ['Купить молоко', 'Купить хлеб'])
 
    def test_active_supports_search(self):
        response = self.client.get(reverse('note-active'), {'search': 'молоко'})
        self.assertEqual(response.data['count'], 1)
 
    def test_stats_counts_only_own_notes(self):
        response = self.client.get(reverse('note-stats'))
        self.assertEqual(response.data['total'], 3)
        self.assertEqual(response.data['done'], 1)
 
    def test_numeric_title_is_rejected(self):
        response = self.client.post(reverse('note-list'), {'title': '12345'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['title'][0], 'Заголовок не может быть числом')
