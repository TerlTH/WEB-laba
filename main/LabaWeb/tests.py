from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Note

class NoteAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.note = Note.objects.create(title='Тест', content='Описание')

    def test_get_notes_list(self):
        """GET /api/notes/ должен быть доступен без авторизации"""
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note_detail(self):
        """GET /api/notes/<id>/ должен вернуть конкретную заметку"""
        response = self.client.get(f'/api/notes/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тест')

    def test_create_note_unauthorized(self):
        """POST без токена должен вернуть 401"""
        response = self.client.post('/api/notes/', {'title': 'Без токена', 'content': '...'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_note_with_token(self):
        """POST с токеном должен создать заметку"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/api-token-auth/', {'username': 'testuser', 'password': 'testpass'})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.post('/api/notes/', {'title': 'Новая', 'content': 'Контент'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)

    def test_update_note(self):
        """PUT с токеном должен обновить заметку"""
        self.client.login(username='testuser', password='testpass')
        token = self.client.post('/api-token-auth/', {
            'username': 'testuser', 'password': 'testpass'
        }).data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.put(f'/api/notes/{self.note.id}/', {
            'title': 'Обновлено', 'content': 'Новый текст'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Обновлено')

    def test_delete_note(self):
        """DELETE с токеном должен удалить заметку"""
        self.client.login(username='testuser', password='testpass')
        token = self.client.post('/api-token-auth/', {
            'username': 'testuser', 'password': 'testpass'
        }).data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.delete(f'/api/notes/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
