from django.shortcuts import render
from blogs.models import Blog,Category
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