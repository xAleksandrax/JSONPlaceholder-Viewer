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

        
class TestPostsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_get_posts_with_comments_and_users_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)
    
    def test_get_posts_with_comments_and_users_authenticated_with_limit(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('posts', args=[4]))
        self.assertEqual(response.status_code, 200)

    def test_get_posts_with_comments_and_users_unauthenticated(self):
        response = self.client.get(reverse('posts'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('posts')}")
        # reverse generuje adres url jeśli taki jest przypisany w urls.py

    def test_get_posts_with_comments_and_users_unauthenticated_with_limit(self):
        response = self.client.get(reverse('posts', args=[4]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('posts', args=[4])}")

    def test_get_user_albums_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('albums'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_albums.html')
        # sprawdza czy używany jest poprawny szablon

    def test_get_user_albums_unauthenticated(self):
        response = self.client.get(reverse('albums'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('albums')}") 
        # sprawdza czy następuje przekierowanie na dobry URL

    def test_get_comments_for_post_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('comments', args=[4]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments.html')

    def test_get_comments_for_post_unauthenticated(self):
        response = self.client.get(reverse('comments', args=[4]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('comments', args=[4])}")

