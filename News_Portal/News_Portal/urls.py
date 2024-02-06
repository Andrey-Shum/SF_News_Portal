"""
Конфигурация URL для проекта News_Portal.

Список `urlpatterns` направляет URL-адреса в представления.
Для получения дополнительной информации см.:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Примеры:
Представления функций
    1. Добавить импорт: из представлений импорта my_app
    2. Добавьте URL-адрес в urlpatterns: path('', views.home, name='home')
Представления на основе классов
    1. Добавить импорт: from other_app.views import Home
    2. Добавьте URL-адрес в urlpatterns: path('', Home.as_view(), name='home')
Включение другой конфигурации URL
    1. Импортируйте функцию include(): из django.urls import include, path
    2. Добавьте URL-адрес в urlpatterns: path('blog', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('accounts/', include('allauth.urls')),  # Запросы от пользователей по
    # ссылкам, которые начинаются с /accounts/
    path('subscriptions/', include('subscriptions.urls')),
]
