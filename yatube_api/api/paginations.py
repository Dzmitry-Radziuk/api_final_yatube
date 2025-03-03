from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class PostPagination(LimitOffsetPagination):
    """Не возвращает обертку, если лимит и офсет не заданы."""
    def get_paginated_response(self, data):
        if self.limit is None and self.offset is None:
            return Response(data)
        return super().get_paginated_response(data)
