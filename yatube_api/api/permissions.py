from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Изменять или удалять ресурс может только автор."""

    def has_object_permission(self, request, view, obj):
        """Проверяет, имеет ли пользователь право на доступ к объекту."""
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        return obj.author == request.user
