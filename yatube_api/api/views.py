from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from api.paginations import PostPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Group, Post


class BaseViewSet(viewsets.ModelViewSet):
    """Базовый вьюсет с общей логикой для аутентификации и фильтрации."""

    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]

    def perform_create(self, serializer):
        """Общий метод для сохранения объектов с текущим пользователем."""
        serializer.save(user=self.request.user)


class FollowViewSet(BaseViewSet):
    """ViewSet для работы с подписками пользователей."""

    serializer_class = FollowSerializer
    search_fields = ('following__username',)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Возвращает подписки текущего пользователя."""
        return self.request.user.followers.all()


class PostListViewSet(BaseViewSet):
    """ViewSet для работы с постами."""

    queryset = Post.objects.select_related('author')
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = PostPagination

    def perform_create(self, serializer):
        """Создаёт пост с текущим пользователем как автором."""
        serializer.save(author=self.request.user)


class CommentListViewSet(BaseViewSet):
    """ViewSet для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_post(self, post_id):
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        """Возвращает комментарии для конкретного поста."""
        post_id = self.kwargs.get('post_id')
        post = self.get_post(post_id)
        return post.comments.select_related('author')

    def perform_create(self, serializer):
        """Создаёт комментарий для поста с текущим пользователем(автором)."""
        post_id = self.kwargs.get('post_id')
        post = self.get_post(post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с группами."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)
