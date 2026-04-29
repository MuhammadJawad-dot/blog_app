from django.shortcuts import get_object_or_404, render,redirect

from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required, permission_required
from .form import CategoryForm, PostForm ,AddUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User 


# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    category_count=Category.objects.all().count()
    blogs_count=Blog.objects.all().count()
    context={
        'category_count': category_count,
        'blogs_count': blogs_count
    }
    return render(request,'dashboard/dashboard.html',context)

@login_required(login_url='login')
def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request,'dashboard/categories.html', context)

def add_category(request):
    if request.method == 'POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form=CategoryForm()
    context={
        'form':form
    }
    return render(request,'dashboard/add_category.html',context)

def edit_category(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'dashboard/edit_category.html', context)

def delete_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()
    return redirect('categories')

def posts(request):
    posts = Blog.objects.all()
    context = {'posts': posts}
    return render(request,'dashboard/post.html', context)



def add_post(request):
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            title=form.cleaned_data['title']
            post.slug=slugify(title)+'-'+str(post.id)
            post.save()
            return redirect('posts')
    form=PostForm()
    context={
        'form':form
    }
    return render(request,'dashboard/add_post.html',context)

def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-'+str(post.id)
            post.save()
            return redirect('posts')
    form = PostForm(instance=post)
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'dashboard/edit_post.html', context)

def delete_post(request,pk):
    post=get_object_or_404(Blog,pk=pk)
    post.delete()
    return redirect('posts')

def user(request):
    if not request.user.has_perm('auth.view_user'):
        return render(request, '404.html')
    user=User.objects.all()
    context={
        'user':user
    }
    return render(request,'dashboard/user.html',context)

@permission_required('auth.add_user', login_url='login')
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user')
    form = AddUserForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/add_user.html', context)

@permission_required('auth.change_user', login_url='login')
def edit_user(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AddUserForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('user')
    form = AddUserForm(instance=user_obj)
    context = {
        'form': form,
        'user_obj': user_obj
    }
    return render(request, 'dashboard/edit_user.html', context)

@permission_required('auth.delete_user', login_url='login')
def delete_user(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    user_obj.delete()
    return redirect('user')