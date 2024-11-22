from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()
    
    def get_stats(self):
        # Statistiques de base
        basic_stats = {
            'posts_count': self.posts.count(),
            'followers_count': self.followers.count(),
            'following_count': self.following.count(),
        }
        
        # Statistiques d'interaction
        interaction_stats = {
            'likes_given': self.likes.count(),
            'likes_received': sum(post.likes.count() for post in self.posts.all()),
            'comments_made': self.comments.count(),
            'comments_received': sum(post.comments.count() for post in self.posts.all()),
        }
        
        # Statistiques des hashtags
        hashtag_stats = {
            'unique_hashtags_used': self.posts.values('hashtags__name').distinct().count(),
            'total_hashtags_used': sum(post.hashtags.count() for post in self.posts.all()),
        }
        
        # Statistiques d'engagement
        engagement_stats = {
            'avg_likes_per_post': round(interaction_stats['likes_received'] / basic_stats['posts_count'], 2) if basic_stats['posts_count'] > 0 else 0,
            'avg_comments_per_post': round(interaction_stats['comments_received'] / basic_stats['posts_count'], 2) if basic_stats['posts_count'] > 0 else 0,
        }
        
        return {
            **basic_stats,
            **interaction_stats,
            **hashtag_stats,
            **engagement_stats,
        }

    def get_recent_activity(self):
        recent_posts = self.posts.order_by('-created_at')[:5]
        recent_likes = self.likes.order_by('-created_at')[:5]
        recent_comments = self.comments.order_by('-created_at')[:5]
        
        return {
            'recent_posts': recent_posts,
            'recent_likes': recent_likes,
            'recent_comments': recent_comments,
        }

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profil de {self.user.username}'

# Signal pour créer automatiquement un profil quand un utilisateur est créé
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    instance.profile.save()
