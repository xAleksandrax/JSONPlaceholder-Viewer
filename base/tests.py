from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestLoginView(TestCase):
    def setUp(self):
        User.objects.create_user('testuser', password='testpass')

    def test_login(self):
        response = Client().post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('posts'))

class TestRegisterView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')
        self.username = 'testuser'
        self.password = 'testpass123'

    def test_register(self):
        response = self.client.post(self.url, {'username': self.username, 'password1': self.password, 'password2': self.password})
        self.assertRedirects(response, reverse('posts'))

        
class TestPostsView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_get_posts_with_comments_and_users(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)

    def test_get_user_albums_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('albums'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_albums.html')

    def test_get_user_albums_unauthenticated(self):
        response = self.client.get(reverse('albums'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('albums')}")

