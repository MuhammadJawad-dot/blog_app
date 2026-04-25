from django.contrib import auth
from django.shortcuts import redirect, render
from blogs.models import Blog,Category
from .form import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
def home(request):
    category=Category.objects.all()
    featured_post=Blog.objects.filter(is_featured=True, status='published')
    posts=Blog.objects.filter(is_featured=False, status='published')
    context={
        'category':category,
        'featured_post':featured_post,
        'posts':posts
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
    form=RegistrationForm()
    context={        
             'form':form
    }
    return render(request, 'register.html',context)

def login(request):
    if request.method == 'POST':
        form=AuthenticationForm(request, request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    form=AuthenticationForm()
    context={
        'form':form
    }
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')
