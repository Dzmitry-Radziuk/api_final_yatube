from django.db import IntegrityError
from django.http import Http404
from rest_framework.exceptions import (NotAuthenticated, PermissionDenied,
                                       ValidationError)
from rest_framework.views import exception_handler


class FollowAlreadyExistsError(ValidationError):
    """Выбрасывается, когда пользователь уже подписан на другого."""
    def __init__(self, detail="Вы уже подписаны на этого пользователя."):
        super().__init__({"detail": detail})


class SelfFollowError(ValidationError):
    """Выбрасывается при попытке подписаться на себя."""
    def __init__(self, detail="Нельзя подписаться на самого себя!"):
        super().__init__({"detail": detail})


def api_exception_handler(exc, context):
    """Обработчик исключений, который модифицирует стандартный ответ."""
    response = exception_handler(exc, context)

    if response is not None:
        process_error_response(exc, response)

    return response


def process_error_response(exc, response):
    """Обрабатывает различные типы ошибок и изменяет их ответы."""
    if isinstance(exc, NotAuthenticated):
        response.data = {'detail': "Учетные данные не были предоставлены."}

    elif isinstance(exc, ValidationError):
        handle_validation_error(response)

    elif isinstance(exc, IntegrityError):
        if "UNIQUE constraint failed" in str(exc):
            raise FollowAlreadyExistsError(
                "Вы уже подписаны на этого пользователя.")
        return None

    elif isinstance(exc, Http404):
        response.data = {'detail': "Страница не найдена"}

    elif isinstance(exc, PermissionDenied):
        response.data = {
            'detail': (
                "У вас недостаточно прав для выполнения данного действия."
            )
        }
        response.status_code = 403


def handle_validation_error(response):
    """Обрабатывает ошибки валидации, изменяя сообщения об ошибках."""
    if isinstance(response.data, dict):
        for field, messages in response.data.items():
            for idx, message in enumerate(messages):
                if message == "This field is required.":
                    messages[idx] = "Обязательное поле."
