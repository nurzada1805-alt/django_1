import os
import shutil
import tempfile
 
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
 
from notes.models import Note
 
from .base import NotesAPITestCase
 
MEDIA_ROOT = tempfile.mkdtemp()
 
 
@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class DeleteAttachmentTests(NotesAPITestCase):
 
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
 
    def setUp(self):
        super().setUp()
        self.masha_note.attachment = SimpleUploadedFile('list.txt', b'milk')
        self.masha_note.save()
        self.path = self.masha_note.attachment.path
        self.url = reverse('note-delete-attachment', args=[self.masha_note.pk])
 
    def test_author_deletes_attachment(self):
        self.client.force_authenticate(user=self.masha)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.masha_note.refresh_from_db()
        self.assertFalse(self.masha_note.attachment)       # поле пустое
        self.assertFalse(os.path.exists(self.path))        # файла на диске нет
 
    def test_other_user_gets_404(self):
        self.client.force_authenticate(user=self.dima)
        self.assertEqual(self.client.delete(self.url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(os.path.exists(self.path))
 
    def test_admin_gets_403(self):
        self.client.force_authenticate(user=self.admin)
        self.assertEqual(self.client.delete(self.url).status_code, status.HTTP_403_FORBIDDEN)
 
    def test_deleting_note_deletes_file(self):  # задание со звёздочкой
        self.client.force_authenticate(user=self.masha)
        self.client.delete(reverse('note-detail', args=[self.masha_note.pk]))
        self.assertFalse(Note.objects.filter(pk=self.masha_note.pk).exists())
        self.assertFalse(os.path.exists(self.path))
