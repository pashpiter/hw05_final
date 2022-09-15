from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Follow, Group, Post, Comment
from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm

POSTS_PER_PAGE: str = 10
User = get_user_model()


def paginator(post_list, request) -> dict:
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


@cache_page(5, key_prefix='index_page')
def index(request):
    post_list = Post.objects.select_related('author')
    page_obj = paginator(post_list, request)
    context = {
        'page_obj': page_obj,
    }
    template = 'posts/index.html'
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all().select_related('group')
    page_obj = paginator(post_list, request)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    user = get_object_or_404(User, username=username)
    post_list = user.posts.select_related('author', 'group')
    page_obj = paginator(post_list, request)
    following = None
    if request.user.is_authenticated:
        following = Follow.objects.filter(user=request.user, author=user)
    context = {
        'author': user,
        'page_obj': page_obj,
        'following': following,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    # Для создания кнопки редактирования на страницы поста, только для автора
    is_edit = None
    form = CommentForm(request.POST or None)
    if post.author == request.user:
        is_edit = True
    context = {
        'post': post,
        'is_edit': is_edit,
        'form': form,
    }
    return render(request, template, context)


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    if request.user != author:
        redirect('posts:post_detail', post_id)
    post.delete()
    # Post.objects.filter(post_id=post_id).delete()
    return redirect('posts:profile', author)


@login_required
def post_create(request):
    template = 'posts/post_create.html'
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user)
        return render(request, template, {'form': form})
    form = PostForm()
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    template = 'posts/post_create.html'
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    if request.user != post.author:
        return redirect('posts:post_detail', post.pk)
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        return redirect('posts:post_detail', post.pk)
    context = {
        'form': form,
        'is_edit': is_edit
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, pk=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def comment_delete(request, post_id, comment_id):
    get_object_or_404(Comment, pk=comment_id).delete()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    page_obj = paginator(post_list, request)
    context = {
        'page_obj': page_obj,
    }
    template = 'posts/follow.html'
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author == request.user:
        return redirect('posts:profile', username=author)
    Follow.objects.get_or_create(
        user=request.user,
        author=author
    )
    return redirect('posts:profile', username=author)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username=author)
