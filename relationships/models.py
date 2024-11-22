from django.db import models

class Follow(models.Model):
    follower = models.ForeignKey('accounts.User', related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey('accounts.User', related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following') 