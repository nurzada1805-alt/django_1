from rest_framework import status
from rest_framework.reverse import reverse
from notes.models import Note
from .base import NotesAPITestCase  

class PracticeTests(NotesAPITestCase):
 
    def test_anonymous_cannot_create(self):
        count_before = Note.objects.count()
        response = self.client.post(reverse('note-list'), {'title': 'Аноним'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Note.objects.count(), count_before)
 
    def test_unknown_note_returns_404(self):
        self.client.force_authenticate(user=self.masha)
        response = self.client.get(reverse('note-detail', args=[999999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


        