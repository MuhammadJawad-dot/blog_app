from django.shortcuts import get_object_or_404, render
from .models import Blog,Category
from django.http import HttpResponse
# Create your views here.
def posts_by_category(request, category_id):
    posts = Blog.objects.filter(status='published', category_id=category_id)
    selected_category=get_object_or_404(Category, pk=category_id)
    context={
        'posts': posts,
        'selected_category': selected_category
    }
    return render(request, 'posts_by_category.html', context)