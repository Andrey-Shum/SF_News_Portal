from rest_framework import serializers

from .models import Post, Author


class PostSerializer(serializers.ModelSerializer):
    # для автоматического заполнения поля автор текущим пользователем
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # создаётся скрытое поле HiddenField и в нём по умолчанию прописывается
    # текущий пользователь CurrentUserDefault

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'type', 'content')

    def create(self, validated_data):
        # Получить или создать экземпляр Author для текущего пользователя.
        author, created = Author.objects.get_or_create(
            autUser=self.context['request'].user)
        # Назначьте экземпляр Author для validated_data.
        validated_data['author'] = author
        return super().create(validated_data)
