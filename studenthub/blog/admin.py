from django.contrib import admin
from .models import Post, PostComment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'comment_count')
    list_filter = ('created_at',)
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    
    def comment_count(self, obj):
        return obj.comment_count
    comment_count.short_description = 'Comments'


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'author__username', 'post__title')
    date_hierarchy = 'created_at'
