from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    body = models.TextField(max_length=5000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked_posts', through='Like', blank=True)

    def __str__(self):
        return self.title

    @property
    def likes(self):
        return self.users_like.count()

    class Meta:
        ordering = ['created_at']


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE)
