from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post

from .exceptions import SelfFollowError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Содержит только имя пользователя"""
    class Meta:
        model = User
        fields = ('username',)


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для поста, включая автора и группу."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментария, включая автора."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для группы, включающий все поля модели."""
    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки, включая пользователя и подписку."""
    following = serializers.SlugRelatedField(queryset=User.objects.all(),
                                             slug_field='username')
    user = serializers.SerializerMethodField()

    def validate(self, attrs):
        """Проверяет, что пользователь не может подписаться на себя."""
        user = self.context['request'].user
        following = attrs['following']
        if user == following:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя!")
        return attrs

    def create(self, validated_data):
        """Создает подписку, если она еще не существует."""
        user = self.context['request'].user
        following = validated_data['following']
        follow, created = Follow.objects.get_or_create(
            user=user, following=following)

        if not created:
            raise SelfFollowError("Вы уже подписаны на этого пользователя.")
        return follow

    def get_user(self, obj):
        """Возвращает имя пользователя, связанного с подпиской."""
        return obj.user.username

    class Meta:
        model = Follow
        fields = ('user', 'following')
