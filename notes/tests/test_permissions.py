from django.urls import reverse
from rest_framework import status
 
from notes.models import Note
 
from .base import NotesAPITestCase
 
 
class NotePermissionTests(NotesAPITestCase):
 
    def test_anonymous_gets_401(self):
        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
 
    def test_user_sees_only_own_notes(self):
        self.client.force_authenticate(user=self.masha)
        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [note['title'] for note in response.data['results']]
        self.assertEqual(titles, ['Купить хлеб'])
 
    def test_foreign_note_returns_404(self):
        self.client.force_authenticate(user=self.dima)
        url = reverse('note-detail', args=[self.masha_note.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
 
    def test_admin_reads_but_cannot_edit_foreign_note(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('note-detail', args=[self.masha_note.pk])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
        response = self.client.patch(url, {'title': 'Взлом'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.masha_note.refresh_from_db()
        self.assertEqual(self.masha_note.title, 'Купить хлеб')
 
    def test_author_can_delete_own_note(self):
        self.client.force_authenticate(user=self.masha)
        url = reverse('note-detail', args=[self.masha_note.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(pk=self.masha_note.pk).exists())
 
 
class CategoryPermissionTests(NotesAPITestCase):
 
    def test_user_cannot_create_category(self):
        self.client.force_authenticate(user=self.masha)
        response = self.client.post(reverse('category-list'),
                                    {'name': 'Дом', 'slug': 'home'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
 
    def test_admin_can_create_category(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse('category-list'),
                                    {'name': 'Дом', 'slug': 'home'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




