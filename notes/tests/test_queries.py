from django.urls import reverse
 
from notes.models import Category, Note
 
from .base import NotesAPITestCase
 
 
class QueryCountTests(NotesAPITestCase):
    """Число SQL-запросов не должно расти вместе с числом объектов."""
 
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.masha)
 
    def make_notes(self, count):
        Note.objects.bulk_create([
            Note(title=f'Заметка {i}', author=self.masha, category=self.work)
            for i in range(count)
        ])
 
    def test_note_list(self):
        self.make_notes(3)
        with self.assertNumQueries(2):          # COUNT для пагинации + SELECT
            self.client.get(reverse('note-list'))
        self.make_notes(20)
        with self.assertNumQueries(2):
            self.client.get(reverse('note-list'))
 
    def test_category_list(self):
        Category.objects.bulk_create([
            Category(name=f'Категория {i}', slug=f'cat-{i}') for i in range(10)
        ])
        with self.assertNumQueries(1):
            self.client.get(reverse('category-list'))
 
    def test_stats(self):
        self.make_notes(5)
        with self.assertNumQueries(2):
            response = self.client.get(reverse('note-stats'))
        self.assertEqual(response.data['total'], 6)
        self.assertEqual(response.data['done'], 0)
        self.assertEqual(response.data['active'], 6)
 
 
class CategoryCountTests(NotesAPITestCase):
 
    def test_notes_count_is_personal(self):
        Note.objects.create(title='Маша: работа 2', author=self.masha, category=self.work)
        Note.objects.create(title='Дима: работа', author=self.dima, category=self.work)
        self.client.force_authenticate(user=self.masha)
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.data[0]['notes_count'], 2)   # чужая не считается
        self.client.force_authenticate(user=self.dima)
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.data[0]['notes_count'], 1)
 
    def test_anonymous_cannot_read_categories(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 401)
 
    def test_nested_category_has_no_count(self):
        self.client.force_authenticate(user=self.masha)
        response = self.client.get(reverse('note-detail', args=[self.masha_note.pk]))
        self.assertEqual(response.data['category'], {'id': self.work.pk, 'name': 'Работа',
                                                      'slug': 'work'})
 
    def test_admin_create_response(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse('category-list'),
                                    {'name': 'Дом', 'slug': 'home'}, format='json')
        self.assertEqual(response.status_code, 201)
        # объект только что создан и не проходил через annotate() — поля нет
        self.assertNotIn('notes_count', response.data)
 
    def test_order_by_notes_count(self):
        home = Category.objects.create(name='Дом', slug='home')
        for i in range(2):
            Note.objects.create(title=f'Дома {i}', author=self.masha, category=home)
        self.client.force_authenticate(user=self.masha)
        response = self.client.get(reverse('category-list'), {'ordering': '-notes_count'})
        self.assertEqual([c['slug'] for c in response.data], ['home', 'work'])
