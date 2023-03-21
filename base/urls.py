from django.urls import path
from .views import get_posts, Login, Register, LogoutView

urlpatterns = [
    path('', get_posts, name='posts'),
    #logowanie, rejestracja
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', Register.as_view(), name='register')
]