from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Изменять или удалять ресурс может только автор."""
    # У меня только вот с этим вариантом тесты проходит, если вьюхи не менять.
    # Если можно, напишите, как бы Вы сделали, в комментах к ревью
    # или в пачке.
    # Спасибо за подробные комментарии и полезные ссылки!)
    def has_object_permission(self, request, view, obj):
        """Разрешает безопасные методы всем, а изменение — только автору."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
