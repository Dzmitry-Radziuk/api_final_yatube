from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    list_filter = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date', 'group')
    search_fields = ('text', 'author__username')
    list_filter = ('pub_date', 'author', 'group')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created', 'text')
    search_fields = ('author__username', 'text')
    list_filter = ('created', 'author')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
