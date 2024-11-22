from django.db import models
from django.conf import settings
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField('Hashtag', related_name='posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Post de {self.user.username} ({self.created_at})'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def get_likes_count(self):
        return self.post_likes.count()

    def is_liked_by_user(self, user):
        return self.post_likes.filter(user=user).exists()

    def get_comments_count(self):
        return self.post_comments.count()

class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'#{self.name}'

    def get_absolute_url(self):
        return reverse('hashtag_posts', args=[self.name])

    @property
    def post_count(self):
        return self.posts.count()
