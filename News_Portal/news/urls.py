from django.urls import path
from django.views.decorators.cache import cache_page
from . import views
from .views import NewsList, NewsDetail, Search, NewsEdit, NewsDelete, ArticleEdit, ArticleDelete

app_name = 'news'

urlpatterns = [
    path('', views.Start_Padge, name='Start'),  # URL-шаблон Стартовой страницы
    path('search/', Search.as_view(), name='search'),  # URL-шаблон Поисковой страницы
    path('news/', NewsList.as_view(), name='news_list'),  # URL-шаблон для списка новостей
    path('news/<int:pk>/', cache_page(60*5)(NewsDetail.as_view()), name='news_detail'),
    # URL-шаблон списка новостей
    path('article/', views.article_list, name='article_list'),  # URL-шаблон для списка статей
    path('articles/<int:post_id>/', views.article_detail, name='article_detail'),
    # URL-шаблон для статьи
    path('news/create/', views.NewsCreate.as_view(), name='news_create'),
    # URL-шаблон для создания новостей
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    # URL-шаблон для редактирования новостей
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    # URL-шаблон для удаления новостей
    path('articles/create/', views.ArticleCreate.as_view(), name='articles_create'),
    # URL-шаблон для создания статьи
    path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    # URL-шаблон для редактирования статьи
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    # URL-шаблон для удаления статьи

]
