from django.urls import include, path
from rest_framework import routers

from api.views import (CommentListViewSet, FollowViewSet, GroupViewSet,
                       PostListViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostListViewSet, basename='posts')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentListViewSet, basename='comments'
)
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register('follow', FollowViewSet, basename='follow')
urlpatterns = [

    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
]
