import requests
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.list import ListView
from django import forms
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from .models import Project
from django.contrib.auth.decorators import login_required


def get_posts(request):
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = response.json()
    return render(request, 'posts.html', {'posts': posts})

def get_comments(request):
    response = requests.get('https://jsonplaceholder.typicode.com/comments')
    comments = response.json()
    return render(request, 'posts.html', {'comments': comments})

def get_albums(request):
    response = requests.get('https://jsonplaceholder.typicode.com/albums')
    albums = response.json()
    return render(request, 'albums.html', {'albums': albums})

def get_photos(request):
    response = requests.get('https://jsonplaceholder.typicode.com/photos')
    photos = response.json()
    return render(request, 'photos.html', {'photos': photos})

def get_users(request):
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    users = response.json()
    return render(request, 'users.html', {'users': users})

import requests

@login_required(login_url = 'login')
def get_posts_with_comments_and_users(request):
    # get posts
    posts_response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = posts_response.json()

    # get comments
    comments_response = requests.get('https://jsonplaceholder.typicode.com/comments')
    comments = comments_response.json()

    # get users
    users_response = requests.get('https://jsonplaceholder.typicode.com/users')
    users = users_response.json()

    # create a dictionary to store the users by id
    users_dict = {user['id']: user for user in users}

    # create a dictionary to store the comments by post id
    comments_dict = {}
    for comment in comments:
        post_id = comment['postId']
        if post_id not in comments_dict:
            comments_dict[post_id] = []
        comments_dict[post_id].append(comment)

    # add the comments and user info to each post
    for post in posts:
        post['comments'] = comments_dict.get(post['id'], [])
        post['user'] = users_dict.get(post['userId'], {})

    return render(request, 'posts.html', {'posts': posts})


class Login(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    widgets = {
        'username': forms.TextInput(attrs={'autocomplete': 'off'}),
        'password': forms.PasswordInput(attrs={'autocomplete': 'off'}),
    }

    def get_success_url(self):
        return reverse_lazy('posts')

class Register(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('posts')
    

    def form_valid(self, form):
        if form.save() is not None:
            login(self.request, form.save())
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('posts')
        return super(Register, self).get(*args, **kwargs)