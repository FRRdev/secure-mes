from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Post(models.Model):
    """ Post model
    """
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
    """ Like model
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'Like from {self.user}'


class Comment(MPTTModel):
    """ Comment model
    """
    text = models.TextField(max_length=512)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return "{} - {}".format(self.user, self.post)
