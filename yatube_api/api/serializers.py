from api.exceptions import SelfFollowError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для поста, включая автора и группу."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментария, включая автора."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для группы, включающий все поля модели."""

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки, включая пользователя и подписку."""

    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    user = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        exclude = ('id',)

    def get_user(self, obj):
        """Возвращает имя пользователя, связанного с подпиской."""
        return obj.user.username

    def validate_following(self, value):
        """Проверяет, что пользователь не может подписаться на себя."""
        user = self.context['request'].user
        if user == value:
            raise SelfFollowError()

        if Follow.objects.filter(user=user, following=value).exists():
            raise SelfFollowError()

        return value
