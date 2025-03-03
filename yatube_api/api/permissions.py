from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Изменять или удалять ресурс может только автор."""

    def has_object_permission(self, request, view, obj):
        """Проверяет, имеет ли пользователь право на доступ к объекту."""
        return (request.user and request.user.is_authenticated
                and obj.author == request.user)
