from django.contrib import admin
from .models import Resource, Tag, Comment


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'upvote_count', 'comment_count')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'description', 'author__username')
    date_hierarchy = 'created_at'
    filter_horizontal = ('tags', 'upvotes')
    
    def upvote_count(self, obj):
        return obj.upvote_count
    upvote_count.short_description = 'Upvotes'
    
    def comment_count(self, obj):
        return obj.comment_count
    comment_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'resource', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'author__username', 'resource__title')
    date_hierarchy = 'created_at'
