

from django.shortcuts import get_object_or_404, render
from .models import Blog,Category
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
def posts_by_category(request, category_id):
    posts = Blog.objects.filter(status='published', category_id=category_id)
    selected_category=get_object_or_404(Category, pk=category_id)
    context={
        'posts': posts,
        'selected_category': selected_category
    }
    return render(request, 'posts_by_category.html', context)

def blogs(request,slug):
     single_blog=get_object_or_404(Blog,slug=slug,status='published')
     context={
         'single_blog':single_blog
     }
     return render(request,'blogs.html',context)
 
 
def search(request):
    keyword = request.GET.get('keyword', '').strip()
    blogs = Blog.objects.none()
    if keyword:
        # Split keyword into individual words and search for each
        terms = keyword.split()  # ✅ handles multiple spaces between words
        query = Q()
        for term in terms:
            query |= (
                Q(title__icontains=term) |
                Q(short_description__icontains=term) |
                Q(blog_body__icontains=term)
            )
        blogs = Blog.objects.filter(query, status='published').distinct()
    
    # if keyword:
    #     blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='published')
    
    context = {
        'blogs': blogs,
        'keyword': keyword,
    }
    return render(request, 'search.html', context)

