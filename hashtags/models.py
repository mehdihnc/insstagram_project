from django.db import models

class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    posts = models.ManyToManyField('posts.Post', related_name='hashtags')
    created_at = models.DateTimeField(auto_now_add=True) 