from django.urls import include, path
from rest_framework import routers

from .views import (CommentListViewSet, FollowViewSet, GroupViewSet,
                    PostListViewSet)

router = routers.DefaultRouter()
router.register(r'posts', PostListViewSet, basename='posts')
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentListViewSet, basename='comments'
)
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'follow', FollowViewSet, basename='follow')
urlpatterns = [
    path('', include(router.urls)),
]
