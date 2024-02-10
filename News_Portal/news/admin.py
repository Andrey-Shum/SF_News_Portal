from django.contrib import admin

from .models import Author, Category, Post, Comment
from django.db.models import F


# напишем уже знакомую нам функцию обнуления рейтинга поста
def nullify_rating(modeladmin, request, queryset):
    # Все аргументы уже должны быть вам знакомы, самые нужные из них
    # это request — объект хранящий информацию о запросе
    # и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating=0)


def up_rating(modeladmin, request, queryset):
    # Увеличиваем поле рейтинга на 1 для выбранных объектов.
    queryset.update(rating=F('rating') + 1)


def down_rating(modeladmin, request, queryset):
    # Уменьшаем поле рейтинга на 1 для выбранных объектов.
    queryset.update(rating=F('rating') - 1)


def nullify_ratingA(modeladmin, request, queryset):
    queryset.update(ratingAut=0)


def up_ratingA(modeladmin, request, queryset):
    # Увеличиваем поле рейтинга на 1 для выбранных объектов.
    queryset.update(ratingAut=F('ratingAut') + 1)


def down_ratingA(modeladmin, request, queryset):
    # Уменьшаем поле рейтинга на 1 для выбранных объектов.
    queryset.update(ratingAut=F('ratingAut') - 1)


nullify_rating.short_description = 'Обнулить рейтинг'
up_rating.short_description = 'Увеличить рейтинг на 1'
down_rating.short_description = 'Уменьшить рейтинг на 1'
nullify_ratingA.short_description = 'Обнулить рейтинг'
up_ratingA.short_description = 'Увеличить рейтинг на 1'
down_ratingA.short_description = 'Уменьшить рейтинг на 1'

# описание для более понятного представления в админ панеле задаётся,
# как будто это объект.


# Зарегистрируйте свои модели здесь.
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями,
    # которые вы хотите видеть в таблице с товарами
    list_display = ('author', 'type', 'title', 'rating')
    # оставляем только нужные поля
    list_filter = ('author', 'type', 'creationDate', 'rating')
    # добавляем примитивные фильтры в нашу админку
    search_fields = ('author', 'type', 'creationDate', 'rating')
    # добавляем действия в список
    actions = [
        nullify_rating,
        up_rating,
        down_rating
    ]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('autUser', 'ratingAut')
    list_filter = ('autUser', 'ratingAut')
    search_fields = ('autUser', 'ratingAut')
    actions = [
        nullify_ratingA,
        up_ratingA,
        down_ratingA
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'commentPost',
        'commentUser',
        'text',
        'dateCreation',
        'rating'
    )
    list_filter = ('commentPost', 'commentUser', 'dateCreation', 'rating')
    search_fields = ('commentPost', 'commentUser', 'dateCreation', 'rating')
    actions = [
        nullify_rating,
        up_rating,
        down_rating
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
