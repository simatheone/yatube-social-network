from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import (
    get_object_or_404, redirect, render
)
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User
from yatube.settings import POSTS_ON_PAGE


def paginator(request, object):
    """
    Функция, которая возвращает объект класса Paginator.
    Число отоброжаемых объектов на странице равно 10.
    """
    paginator = Paginator(object, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


@cache_page(20)
def index(request):
    """
    Функция, которая возвращает главную страницу,
    на которой отображены 10 постов, отсортированных по дате,
    в порядке убывания.
    Для переключения между страницами с постами добавлен Paginator.
    """
    posts = Post.objects.all()
    page_obj = paginator(request, posts)
    template = 'posts/index.html'
    context = {
        'title': 'Последние обновления на сайте',
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """
    Функция, которая возвращает страницу со всеми постами группы.
    На страницу выводятся 10 записей,
    отсортированных по дате, в порядке убывания.
    Для переключения между страницами с постами добавлен Paginator.
    """
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    page_obj = paginator(request, posts)
    context = {
        'title': 'Записи сообщества',
        'group': group,
        'page_obj': page_obj,
    }
    template = 'posts/group_list.html'
    return render(request, template, context)


def profile(request, username):
    """
    Функция, которая возвращает страницу профиля пользователя
    с 10 постами на странице.
    Посты отсортированы по дате в порядке убывания.
    Для переключения между страницами с постами добавлен Paginator.
    """
    author = get_object_or_404(User, username=username)
    is_follow_obj = []
    show_button = False

    if request.user.is_authenticated:
        show_button = not(request.user.username == username)
        is_follow_obj = Follow.objects.filter(user=request.user, author=author)
    following = bool(is_follow_obj)
    posts = author.posts.all()
    page_obj = paginator(request, posts)
    context = {
        'author': author,
        'page_obj': page_obj,
        'posts': posts,
        'following': following,
        'show_button': show_button
    }
    template = 'posts/profile.html'
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    """
    Функиця, которая отправляет форму с комментарием
    к посту и редиректит на страницу поста.
    """
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


def post_detail(request, post_id):
    """
    Функция, которая возвращает страницу с подробной информацей о посте,
    и подсчитывает колличество постов, написанных данным автором.
    Редактировать пост может только автор поста.
    """
    post = get_object_or_404(Post, pk=post_id)
    count_posts = post.author.posts.count()
    form = CommentForm(
        request.POST or None,
    )
    comments = Comment.objects.filter(post_id=post_id)
    context = {
        'post': post,
        'count_posts': count_posts,
        'form': form,
        'comments': comments,
    }
    template = 'posts/post_detail.html'
    return render(request, template, context)


@login_required
def post_create(request):
    """
    Функиця, которая возвращает страницу с формой создания поста.
    Для создания поста пользователь должен быть залогинен на сайте.
    Правильно заполненная форма сохраняется в базу данных.
    """
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('posts:profile', username=new_post.author)
    template = 'posts/create_post.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    """
    Функция, которая возвращает страницу с формой редактирования поста.
    Для редактирования поста пользователь должен быть залогинен на сайте
    и быть автором данного поста.
    Правильно заполненная форма сохраняется в базу данных.
    """
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    if post.author_id != request.user.id:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    template = 'posts/create_post.html'
    context = {
        'post': post,
        'form': form,
        'is_edit': is_edit,
    }
    return render(request, template, context)


@login_required
def follow_index(request):
    """
    Функиця возвращает страницу с постами на авторов которых
    подписан пользователь.
    """
    posts = Post.objects.filter(author__following__user=request.user)
    page_obj = paginator(request, posts)
    context = {
        'page_obj': page_obj,
    }
    template = 'posts/follow.html'
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """
    Функция дает возможность подписаться на автора,
    если пользователь ранее на него не подсывался.
    При оформлении подписки на автора, редиректит на страницу
    профиля автора.
    """
    template = 'posts:profile'
    author = User.objects.get(username=username)
    if request.user.username != username:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect(template, username=username)


@login_required
def profile_unfollow(request, username):
    """
    Функция дает возможность отписаться от ранее
    подписанного автора. При отписки от автора,
    функция редиректит на страницу профиля автора.
    """
    author = User.objects.get(username=username)
    Follow.objects.get(user=request.user, author=author).delete()
    return redirect('posts:profile', username=username)
