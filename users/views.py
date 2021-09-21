from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegisterForm

# Create your views here.
def home(request):
    return render(request, 'users/home.html')

def register(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hey {username}, you account was created!')
            return redirect('home')


    return render(request, 'users/register.html', {'form' : form})


def login(request):
    return render(request, 'users/login.html')

def logout(request):
    return render(request, 'users/logout.html')

def profile(request):
    return render(request, 'users/profile.html')

def info(request):
    return render(request, 'users/info.html')