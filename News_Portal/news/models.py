from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models import Sum
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse

from subscriptions.models import Subscriber
from django.core.cache import cache


# Создавайте свои модели здесь.
class Author(models.Model):
    """
    Метод update_rating() вычисляет суммарный рейтинг каждой статьи автора,
    умножает его на 3, а затем складывает с суммарным рейтингом всех
    комментариев автора и комментариев к статьям автора.
    Результат сохраняется в поле rating объекта Author
    """

    autUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAut = models.SmallIntegerField(default=0)

    def update_rating(self):
        # Вычисление суммарного рейтинга статей автора
        post_sum = self.post_set.aggregate(postRating=Sum('rating'))  # Сбор
        # всех данных определённого поля автора
        temp_sum_p = 0
        temp_sum_p += post_sum.get('postRating')
        # Вычисление суммарного рейтинга комментариев автора
        comment_sum = self.autUser.comment_set.aggregate(commentRating=Sum('rating'))
        temp_sum_c = 0
        temp_sum_c += comment_sum.get('commentRating')

        self.ratingAut = temp_sum_p * 3 + temp_sum_c
        self.save()

    # для удобного отображения на странице администратора
    def __str__(self):
        return self.autUser.username


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    # для отображения имён вместо объектов
    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Метод preview() возвращает начало статьи длиной 124 символа с многоточием в
    конце Методы like() и dislike() увеличивают/уменьшают рейтинг на единицу.
    """
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGOY_CHOICES = (
        ('AR', 'Статья'),
        ('NW', 'Новость'),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Поле Автор
    type = models.CharField(max_length=2,
                            choices=CATEGOY_CHOICES,
                            default=ARTICLE)  # Поле выбора новость / статья
    creationDate = models.DateTimeField(auto_now_add=True)
    # creationDate Авто добавление даты создания
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    content = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:123]} ...'

    # для удобного отображения на странице администратора
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        cache.delete(f'post_{self.id}')
        super().save(*args, **kwargs)
        from .tasks import send_news_notification
        send_news_notification.delay(self.id)

    def delete(self, *args, **kwargs):
        cache.delete(f'post_{self.id}')
        super().delete(*args, **kwargs)

    @staticmethod
    def get_cached_post(post_id):
        # Метод для получения кэшированной статьи по id.
        # Проверяет, есть ли статья в кэше, если нет,
        # то извлекает из базы данных и сохранять в кэш.
        cache_key = f'post_{post_id}'
        post = cache.get(cache_key)
        if post is None:
            post = Post.objects.filter(id=post_id).first()
            if post is not None:
                cache.set(cache_key, post)
        return post

    # какую страницу нужно открыть после создания
    @staticmethod
    def get_absolute_url():
        return reverse('Start')


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """
    Методы like() и dislike() увеличивают/уменьшают рейтинг на единицу.
    """
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE,
                                    related_name='comments')
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # для удобного отображения на странице администратора
    def __str__(self):
        return self.text

# # отправка писем при публикации новой статьи
# @receiver(m2m_changed, sender=Post.postCategory.through)
# def notify_subscribers(sender, instance, action, **kwargs):
#     if action == "post_add":  # отправка уведомления только при добавлении категорий.
#         # print(f"notify_subscribers вызвали публикацию id={instance.id}")
#         if instance.id:
#             print("Сообщение создано, отправка писем")
#             categories = instance.postCategory.all()
#             if categories:
#                 for category in categories:
#                     subscribers = Subscriber.objects.filter(category=category)
#                     for subscriber in subscribers:
#                         if subscriber.user.email:
#                             print(f"Отправка электронной почты на {subscriber.user.email}")
#                             send_mail(
#                                 'Новый пост в категории, на которую вы подписаны',
#                                 f'Посмотреть можно здесь: http://127.0.0.1:8000/news/{instance.id}',
#                                 'AndreyTestSF@yandex.ru',
#                                 [subscriber.user.email],
#                                 )
#                         else:
#                             print(f"Нет электронной почты для пользователя {subscriber.user.username}")
#             else:
#                 print("Нет категорий для этого сообщения")
#         else:
#             print("Пост не создан, письма не отправляются")
