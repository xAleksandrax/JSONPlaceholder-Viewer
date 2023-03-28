from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestLoginView(TestCase):
    def setUp(self):
        User.objects.create_user('testuser', password='testpass')

    def test_login(self):
        response = Client().post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('posts'))

# class TestPostsView(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.url = reverse('posts')

#     def test_get_posts_with_comments_and_users(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'posts.html')

# class TestRegisterView(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.url = reverse('register')
#         self.username = 'testuser'
#         self.password = 'testpass'

#     def test_register(self):
#         response = self.client.post(self.url, {'username': self.username, 'password1': self.password, 'password2': self.password})
#         self.assertRedirects(response, reverse('posts'))