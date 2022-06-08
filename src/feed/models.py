from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    allowed_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="allowed_posts", null=True)
    likes = GenericRelation('Like')

    def __str__(self):
        return f'Post by {self.user}'

    @property
    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'Like from {self.user}'
