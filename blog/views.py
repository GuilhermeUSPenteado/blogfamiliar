from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from django import forms
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, CategoryForm

class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Selecione uma categoria")

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

def user_list(request):
    users = User.objects.all()
    return render(request, 'blog/user_list.html', {'users': users})

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.is_authenticated and request.user.id == user_id:
        return redirect('profile')
    return render(request, 'user_profile.html', {'user': user})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def logout_view(request):
    logout(request)
    return redirect('base')

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})

def category_detail(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})

# Views funcionais sem Django forms e sem validação de dados:
@login_required
def post_list(request):
    search_query = request.GET.get('search', '')
    posts = Post.objects.filter(Q(title__icontains=search_query)).order_by('-post_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    categories = Category.objects.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'categories': categories})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden()
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    else:
        return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def add_category_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        category = Category.objects.get(name=request.POST['category'])
        post.category = category
        post.save()
        return redirect('post_detail', pk=post.id)
    else:
        categories = Category.objects.all()
        return render(request, 'blog/add_category.html', {'post': post, 'categories': categories})

#Views funcionais utilizando Django forms:
# @login_required
# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})


# Views com as classes genéricas ListView, DetailView, CreateView, UpdateView e DeleteView:
# @login_required
# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/post_list.html'
#     context_object_name = 'posts'

# @login_required
# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'

# @login_required
# class PostCreateView(CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'blog/post_edit.html'

# @login_required
# class PostUpdateView(UpdateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'blog/post_edit.html'

# @login_required
# class PostDeleteView(DeleteView):
#     model = Post
#     template_name = 'blog/post_confirm_delete.html'
#     success_url = reverse_lazy('post_list')
