from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import NotAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from api.paginations import CustomPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Comment, Follow, Group, Post


class BaseViewSet(viewsets.ModelViewSet):
    """
    Базовый вьюсет с общей логикой для аутентификации и фильтрации.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]

    def perform_create(self, serializer):
        """Общий метод для сохранения объектов с текущим пользователем."""
        serializer.save(user=self.request.user)


class FollowViewSet(BaseViewSet):
    """
    ViewSet для работы с подписками пользователей.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    search_fields = ['following__username']

    def get_queryset(self):
        """Возвращает подписки текущего пользователя."""
        return Follow.objects.filter(user=self.request.user)


class PostListViewSet(BaseViewSet):
    """
    ViewSet для работы с постами.
    """
    queryset = Post.objects.select_related('author')
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Создаёт пост с текущим пользователем как автором."""
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        serializer.save(author=self.request.user)


class CommentListViewSet(BaseViewSet):
    """
    ViewSet для работы с комментариями.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        """Возвращает комментарии для конкретного поста."""
        post_id = self.kwargs.get('post_id')
        get_object_or_404(Post, id=post_id)
        return Comment.objects.filter(post_id=post_id).select_related('author')

    def perform_create(self, serializer):
        """Создаёт комментарий для поста с текущим пользователем(автором)."""
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы с группами.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
