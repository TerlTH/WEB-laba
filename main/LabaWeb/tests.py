from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from LabaWeb.models import Note

class NoteAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='otheruser', password='testpass')
        self.note = Note.objects.create(title='Тест', content='Описание', owner=self.user)

        self.login_url = '/api/users/login/'
        self.register_url = '/api/users/register/'
        self.profile_url = '/api/users/profile/'
        self.notes_url = '/api/notes/'

    def auth(self, username='testuser', password='testpass'):
        response = self.client.post('/api-token-auth/', {
            'username': username,
            'password': password
        })
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_register_user(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password': 'newpass',
            'age': 20
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_requires_auth(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_authenticated(self):
        self.auth()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)

    def test_create_note_unauthorized(self):
        response = self.client.post(self.notes_url, {
            'title': 'Без токена', 'content': '...'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_note(self):
        self.auth()
        response = self.client.post(self.notes_url, {
            'title': 'Тестовая', 'content': 'Контент'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_notes_list(self):
        Note.objects.create(title='Заметка 1', content='...', owner=self.user)
        response = self.client.get(self.notes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_notes(self):
        self.auth()
        Note.objects.create(title='ABC', content='...', owner=self.user)
        Note.objects.create(title='DEF', content='...', owner=self.user)
        response = self.client.get(self.notes_url + '?search=ABC')
        self.assertEqual(response.status_code, 200)
        results = response.data.get('results', response.data)
        titles = [note['title'] for note in results]
        self.assertIn('ABC', titles)

    def test_update_own_note(self):
        self.auth()
        note = Note.objects.create(title='Старая', content='...', owner=self.user)
        response = self.client.put(
            f'{self.notes_url}{note.id}/',
            {
                'title': 'Обновлённая',
                'content': 'Новое'
            },
            format='multipart'
)
        self.assertEqual(response.status_code, 200)

    def test_update_other_user_note_forbidden(self):
        self.auth()
        note = Note.objects.create(title='Чужая', content='...', owner=self.user2)
        response = self.client.put(f'{self.notes_url}{note.id}/', {
            'title': 'Хак',
            'content': '!!!'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_delete_note(self):
        self.auth()
        note = Note.objects.create(title='Удалить', content='...', owner=self.user)
        response = self.client.delete(f'{self.notes_url}{note.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Note.objects.filter(id=note.id).exists())