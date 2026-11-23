import shutil
import tempfile
 
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
 
from .base import NotesAPITestCase
 
MEDIA_ROOT = tempfile.mkdtemp()
 
 
@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class AttachmentTests(NotesAPITestCase):
 
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)  # убираем файлы за собой
        super().tearDownClass()
 
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.masha)
        self.url = reverse('note-list')
 
    def test_upload_attachment(self):
        file = SimpleUploadedFile('list.txt', b'milk, bread', content_type='text/plain')
        response = self.client.post(self.url, {'title': 'Покупки', 'attachment': file},
                                    format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['attachment'].startswith('http://testserver/media/'))
        self.assertTrue(response.data['attachment'].endswith('.txt'))
 
    def test_wrong_extension(self):
        file = SimpleUploadedFile('virus.exe', b'MZ...', content_type='application/octet-stream')
        response = self.client.post(self.url, {'title': 'Программа', 'attachment': file},
                                    format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('attachment', response.data)
 
    def test_too_big_file(self):
        file = SimpleUploadedFile('big.pdf', b'x' * (2 * 1024 * 1024 + 1))
        response = self.client.post(self.url, {'title': 'Большой файл', 'attachment': file},
                                    format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['attachment'][0], 'Файл больше 2 МБ')
 
    def test_note_without_file(self):
        response = self.client.post(self.url, {'title': 'Без файла'}, format='json')
        self.assertIsNone(response.data['attachment'])
 
    def test_json_patch_keeps_file(self):
        file = SimpleUploadedFile('list.txt', b'milk', content_type='text/plain')
        response = self.client.post(self.url, {'title': 'Покупки', 'attachment': file},
                                    format='multipart')
        detail = reverse('note-detail', args=[response.data['id']])
        response = self.client.patch(detail, {'title': 'Покупки на неделю'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['attachment'])
