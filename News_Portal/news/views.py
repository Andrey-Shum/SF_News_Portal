from django.core.paginator import Paginator
from django.http import Http404
from django.http.response import \
    HttpResponse  # импортируем респонс для проверки текста
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView

from .filters import PostFilter
from .forms import NewsForm, ArticleForm
from .models import Post, Category

import pytz  # импортируем стандартный модуль для работы с часовыми поясами

from django.views.decorators.cache import cache_page

"""
get_object_or_404 - используется для получения объекта из базы данных по
заданным условиям. Если объект не найден, то функция вызывает исключение
`Http404`, и возвращает страницу с ошибкой 404.
"""

# Создайте свои представления здесь


# ====== Стартовая страница ====================================================
# @cache_page(60)  # кэширование на 1 минут (60 сек)
'''
В аргументы к декоратору передаём количество секунд, которые хотим,
чтобы страница держалась в кэше. Внимание! Пока страница находится в кэше,
изменения, происходящие на ней, учитываться не будут!
'''


def Start_Padge(request):
    timezone_str = request.session.get('django_timezone', 'UTC')
    news = Post.objects.filter(type='NW').order_by('-creationDate')[:4]
    current_timezone = pytz.timezone(timezone_str)
    current_time = timezone.localtime(timezone.now(), timezone=current_timezone)
    return render(
        request,
        'flatpages/Start.html',
        {
            'news': news,
            'current_time': current_time,
            'timezones': pytz.common_timezones,
            'selected_timezone': timezone_str
        },
    )


# ====== Новости ===============================================================
class NewsList(ListView):
    paginate_by = 10
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset().filter(type='NW')
        return queryset.order_by('-creationDate')

    def get(self, request):
        models = Post.objects.filter(type='NW')

        context = {
            'news': models,
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
            # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'news_list.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс,
    #  который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/news')


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    model = Post
    form_class = NewsForm
    template_name = 'news_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.type = 'NW'
        form.instance.author = self.request.user.author
        self.object = form.save()
        # Сохранить публикацию, чтобы у нее был идентификатор.
        form.save(commit=False)
        form.save_m2m()  # Сохранение данных «многие ко многим»
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    raise_exception = True
    model = Post
    form_class = NewsForm
    template_name = 'news_edit.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.type = 'NW'
        form.instance.author = self.request.user.author
        self.object = form.save()
        # Сохранить публикацию, чтобы у нее был идентификатор.
        form.save(commit=False)
        form.save_m2m()  # Сохранение данных «многие ко многим»
        return super().form_valid(form)


class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.add_post',)
    raise_exception = True
    model = Post
    template_name = 'news_delete.html'
    success_url = '/'


# ====== Статьи ================================================================
def article_list(request):
    article = Post.objects.filter(type='AR').order_by(
        '-creationDate')  # Фильтруем только статьи
    # и сортируем по убыванию даты
    paginator = Paginator(article, 2)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(
        request,
        'news/article_list.html',
        {
            'articles': articles,
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
            # добавляем в контекст все доступные часовые пояса
        }
    )


# def article_detail(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     return render(request, 'news/article_detail.html', {'post': post})
def article_detail(request, post_id):
    post = Post.get_cached_post(post_id)
    if post is None:
        raise Http404('Статья не найдена')
    return render(request, 'news/article_detail.html', {'post': post})


class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    model = Post
    form_class = ArticleForm
    template_name = 'article_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.type = 'AR'
        form.instance.author = self.request.user.author
        self.object = form.save()
        # Сохранить публикацию, чтобы у нее был идентификатор.
        form.save(commit=False)
        form.save_m2m()  # Сохранение данных «многие ко многим»
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    raise_exception = True
    model = Post
    form_class = ArticleForm
    template_name = 'article_edit.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.type = 'AR'
        form.instance.author = self.request.user.author
        self.object = form.save()
        # Сохранить публикацию, чтобы у нее был идентификатор.
        form.save(commit=False)
        form.save_m2m()  # Сохранение данных «многие ко многим»
        return super().form_valid(form)


class ArticleDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Post
    template_name = 'article_delete.html'
    success_url = '/'


# ====== Поиск =================================================================
class Search(ListView):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    filterset_class = PostFilter
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET,
                                              queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context[
            'categories'] = Category.objects.all()  # Получение всех категорий
        context = {
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
            # добавляем в контекст все доступные часовые пояса
        }
        return context
