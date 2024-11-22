from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def get_stats(self):
        return {
            'posts_count': self.posts.count(),
            'followers_count': self.followers.count(),
            'following_count': self.following.count(),
            'likes_given': self.likes.count(),
            'comments_count': self.comments.count(),
        } 