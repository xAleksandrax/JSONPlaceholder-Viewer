import requests
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django import forms
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
@login_required(login_url='login')
def get_posts_with_comments_and_users(request, limit=None):
    # get posts
    posts_url = 'https://jsonplaceholder.typicode.com/posts'

    if limit is not None:
        posts_url += f'?_limit={limit}'

    posts_response = requests.get(posts_url)
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


@require_http_methods(["GET"])
@login_required(login_url='login')
def get_comments_for_post(request, post_id):
    # get comments for the specified post id
    comments_url = f'https://jsonplaceholder.typicode.com/comments?postId={post_id}'
    comments_response = requests.get(comments_url)
    comments = comments_response.json()

    return render(request, 'comments.html', {'comments': comments})


@login_required(login_url = 'login')
def get_user_albums(request, limit=None):
    # get albums
    albums_response = requests.get('https://jsonplaceholder.typicode.com/albums')
    albums = albums_response.json()

    # get photos
    photos_response = requests.get('https://jsonplaceholder.typicode.com/photos')
    photos = photos_response.json()

    # get users
    users_response = requests.get('https://jsonplaceholder.typicode.com/users')
    users = users_response.json()

    # create a dictionary to store the users by id
    users_dict = {user['id']: user for user in users}

    # create a dictionary to store the photos by album id
    photos_dict = {}
    for photo in photos:
        album_id = photo['albumId']
        if album_id not in photos_dict:
            photos_dict[album_id] = []
        photos_dict[album_id].append(photo)

    # add the photos and user info to each album
    for album in albums:
        album['photos'] = photos_dict.get(album['id'], [])
        album['user'] = users_dict.get(album['userId'], {})

    return render(request, 'user_albums.html', {'albums': albums})

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