import requests
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django import forms
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView

def posts(request):
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = response.json()
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
        return reverse_lazy('reminders')

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
            return redirect('reminders')
        return super(Register, self).get(*args, **kwargs)