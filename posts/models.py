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

    def format_caption_with_hashtags(self):
        words = self.caption.split()
        formatted_words = []
        for word in words:
            if word.startswith('#'):
                hashtag_name = word[1:]
                formatted_words.append(f'<a href="/hashtag/{hashtag_name}/" class="hashtag">{word}</a>')
            else:
                formatted_words.append(word)
        return ' '.join(formatted_words)

    def extract_hashtags(self):
        """Extrait les hashtags du caption"""
        if not self.caption:
            return []
        words = self.caption.split()
        return [word[1:] for word in words if word.startswith('#')]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour les hashtags après la sauvegarde
        hashtags = self.extract_hashtags()
        for tag_name in hashtags:
            hashtag, _ = Hashtag.objects.get_or_create(name=tag_name.lower())
            self.hashtags.add(hashtag)

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
