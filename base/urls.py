from django.urls import path
from .views import posts, Login, Register, LogoutView

urlpatterns = [
    path('posts/', posts, name='posts'),
    #logowanie, rejestracja
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', Register.as_view(), name='register')
]