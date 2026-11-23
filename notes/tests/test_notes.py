from django.urls import reverse
from rest_framework import status
 
from notes.models import Note
 
from .base import NotesAPITestCase
 
 
class NoteCreateTests(NotesAPITestCase):
 
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.masha)
        self.url = reverse('note-list')
 
    def test_author_is_taken_from_request(self):
        data = {'title': 'Новая заметка', 'author': 'dima'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], 'masha')
        note = Note.objects.get(pk=response.data['id'])
        self.assertEqual(note.author, self.masha)
 
    def test_short_title_is_rejected(self):
        response = self.client.post(self.url, {'title': 'аб'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
 
    def test_cannot_close_note_without_text(self):
        url = reverse('note-done', args=[self.masha_note.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['text'][0], 'Нельзя закрыть заметку без описания')
 
    def test_done_marks_note(self):
        self.masha_note.text = 'Бородинский'
        self.masha_note.save()
        url = reverse('note-done', args=[self.masha_note.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_done'])
 
 
class NoteListTests(NotesAPITestCase):
 
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Note.objects.create(title='Отчёт за месяц', text='до пятницы',
                            is_done=True, author=cls.masha, category=cls.work)
        Note.objects.create(title='Записаться к врачу', author=cls.masha)
 
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.masha)
        self.url = reverse('note-list')
 
    def titles(self, response):
        return sorted(note['title'] for note in response.data['results'])
 
    def test_filter_by_is_done(self):
        response = self.client.get(self.url, {'is_done': 'true'})
        self.assertEqual(self.titles(response), ['Отчёт за месяц'])
 
    def test_filter_by_category_slug(self):
        response = self.client.get(self.url, {'category': 'work'})
        self.assertEqual(self.titles(response), ['Купить хлеб', 'Отчёт за месяц'])
 
    def test_search_in_text(self):
        response = self.client.get(self.url, {'search': 'пятниц'})
        self.assertEqual(self.titles(response), ['Отчёт за месяц'])
 
    def test_ordering_by_title(self):
        response = self.client.get(self.url, {'ordering': 'title'})
        titles = [note['title'] for note in response.data['results']]
        self.assertEqual(titles, ['Записаться к врачу', 'Купить хлеб', 'Отчёт за месяц'])
 
    def test_pagination(self):
        Note.objects.bulk_create(
            [Note(title=f'Заметка {i}', author=self.masha) for i in range(12)]
        )
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 15)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
 
    def test_page_size_is_capped(self):
        Note.objects.bulk_create(
            [Note(title=f'Заметка {i}', author=self.masha) for i in range(60)]
        )
        response = self.client.get(self.url, {'page_size': 1000})
        self.assertEqual(len(response.data['results']), 50)
