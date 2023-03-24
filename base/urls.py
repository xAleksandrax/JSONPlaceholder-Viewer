from django.urls import path
from .views import Login, Register, LogoutView, get_posts_with_comments_and_users, get_user_albums

urlpatterns = [
    path('', get_posts_with_comments_and_users, name='posts'),
    path('albums/', get_user_albums, name='albums'),
    #logowanie, rejestracja
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', Register.as_view(), name='register')
]