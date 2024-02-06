from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView

from .filters import PostFilter
from .forms import NewsForm, ArticleForm
from .models import Post, Category

from django.views.decorators.cache import cache_page

"""
get_object_or_404 - используется для получения объекта из базы данных по
заданным условиям. Если объект не найден, то функция вызывает исключение
`Http404`, и возвращает страницу с ошибкой 404.
"""

# Создайте свои представления здесь


# ====== Стартовая страница ====================================================
@cache_page(60)  # кэширование на 1 минут (60 сек)
def Start_Padge(request):
    news = Post.objects.filter(type='NW').order_by('-creationDate')[:4]
    return render(request, 'flatpages/Start.html', {'news': news})


# ====== Новости ===============================================================
class NewsList(ListView):
    paginate_by = 10
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset().filter(type='NW')
        return queryset.order_by('-creationDate')


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
    return render(request, 'news/article_list.html', {'articles': articles})


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
        form.instance.save()
        # Сохранить публикацию, чтобы у нее был идентификатор.
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
        form.instance.save()
        # Сохранить публикацию, чтобы у нее был идентификатор.
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
        return context
