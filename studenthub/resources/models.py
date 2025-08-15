from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class Resource(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    upvotes = models.ManyToManyField(User, related_name='upvoted_resources', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    @property
    def upvote_count(self):
        return self.upvotes.count()
    
    @property
    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.resource.title}'
    
    class Meta:
        ordering = ['-created_at']
