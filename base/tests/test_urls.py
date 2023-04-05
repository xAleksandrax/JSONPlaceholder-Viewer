from django.test import SimpleTestCase
from django.urls import reverse, resolve
from base.views import get_posts_with_comments_and_users, get_user_albums,get_comments_for_post,get_comments_by_postid , Login, LogoutView, Register

class TestUrls(SimpleTestCase):
    # SimpleTestCase używamy kiedy nie ma interakcji z bazą
    def test_posts_url(self):
        url = reverse('posts')
        self.assertEquals(resolve(url).func, get_posts_with_comments_and_users)

    def test_posts_limit_url(self):
        url = reverse('posts', args=[5])
        self.assertEquals(resolve(url).func, get_posts_with_comments_and_users)

    def test_comments_limit_url(self):
        url = reverse('comments', args=[5])
        self.assertEquals(resolve(url).func, get_comments_for_post)

    def test_comments_by_postId_url(self):
        url = reverse('comments')
        print(resolve(url))
        self.assertEquals(resolve(url).func, get_comments_by_postid)

    def test_albums_url(self):
        url = reverse('albums')
        self.assertEquals(resolve(url).func, get_user_albums)

    def test_login_url(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, Login)
        # .view_class dla widoków opartych o klasy

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_register_url(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, Register)

