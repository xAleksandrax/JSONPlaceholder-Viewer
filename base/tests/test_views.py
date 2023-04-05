from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from unittest.mock import Mock


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

    @patch('requests.get')
    def test_mock_get_posts_with_comments_and_users_authenticated(self, mock_get):
        self.client.login(username='testuser', password='testpass')
        mock_posts_response = [{'id': 1, 'title': 'Test post', 'userId': 1}]
        mock_comments_response = [{'id': 1, 'postId': 1, 'body': 'Test comment', 'email': 'test@example.com'}]
        mock_users_response = [{'id': 1, 'name': 'Test user'}]
        
        mock_responses = [
            Mock(status_code=200, json = Mock(return_value = mock_posts_response)),
            Mock(status_code=200, json = Mock(return_value = mock_comments_response)),
            Mock(status_code=200, json = Mock(return_value = mock_users_response)),
        ]
        mock_get.side_effect = mock_responses
        # side_effect może przyjąć funkcję lub listę obiektów, które powinny być zwrócone przez każde kolejne wywołanie funkcji
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')
        self.assertEqual(response.context['posts'], mock_posts_response)
    
    @patch('requests.get')
    def test_mock_get_posts_with_comments_and_users_unauthenticated(self, mock_get):
        mock_posts_response = [{'id': 1, 'title': 'Test post', 'userId': 1}]
        mock_comments_response = [{'id': 1, 'postId': 1, 'body': 'Test comment', 'email': 'test@example.com'}]
        mock_users_response = [{'id': 1, 'name': 'Test user'}]

        mock_responses = [
            Mock(status_code=200, json = Mock(return_value = mock_posts_response)),
            Mock(status_code=200, json = Mock(return_value = mock_comments_response)),
            Mock(status_code=200, json = Mock(return_value = mock_users_response)),
        ]
        mock_get.side_effect = mock_responses
        response = self.client.get(reverse('posts'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('posts')}")

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

    @patch('requests.get')
    def test_mock_get_user_albums_authenticated(self, mock_get):
        self.client.login(username='testuser', password='testpass')
        mock_albums_response = [{'userId': 1, 'id': 1, 'title': 'Test post'}]
        mock_photos_response = [{'albumId': 1, 'id': 1,  'title': 'Test title', 'url': 'test url', 'thumbnailUrl' : 'test thumbnailUrl'}]
        mock_users_response = [{'id': 1, 'name': 'Test user'}]

        mock_responses = [
            Mock(status_code=200, json = Mock(return_value = mock_albums_response)),
            Mock(status_code=200, json = Mock(return_value = mock_photos_response)),
            Mock(status_code=200, json = Mock(return_value = mock_users_response)),
        ]
        mock_get.side_effect = mock_responses
        # side_effect może przyjąć funkcję lub listę obiektów, które powinny być zwrócone przez każde kolejne wywołanie funkcji
        response = self.client.get(reverse('albums'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_albums.html')
        self.assertEqual(response.context['albums'], mock_albums_response)

    def test_get_comments_for_post_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('comments', args=[4]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments.html')

    def test_get_comments_for_post_unauthenticated(self):
        response = self.client.get(reverse('comments', args=[4]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('comments', args=[4])}")

    def test_get_comments_by_postid_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('comments'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments.html')

    def test_get_comments_by_postid_unauthenticated(self):
        response = self.client.get(reverse('comments'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('comments')}")

    def test_get_comments_by_postid_authenticated_postid_added(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('comments'), {'postId': 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments.html')

    def test_get_comments_by_postid_unauthenticated_postid_added(self):
        response = self.client.get(reverse('comments'), {'postId': 1})
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('comments')}%3FpostId%3D1")
        # kod szesnastkowy aby uniknąć błędów

