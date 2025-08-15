from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self, *args, **kwargs):
        # Ensure default avatar is set if none exists
        if not self.avatar:
            self.avatar = 'avatars/default.png'
        super().save(*args, **kwargs)
