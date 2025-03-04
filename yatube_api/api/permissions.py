from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Изменять или удалять ресурс может только автор."""
    def has_object_permission(self, request, view, obj):
        """Разрешает безопасные методы всем, а изменение — только автору."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
