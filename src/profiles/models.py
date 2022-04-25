from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

from django.db import models

from src.base.services import get_path_upload_avatar


class SecureUser(AbstractUser):
    """Custom user model
    """
    GENDER = (
        ('male', 'male'),
        ('female', 'female')
    )
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), ]
    )
    phone = models.CharField(max_length=12, null=True, blank=True)
    date_of_birth = models.DateField(max_length=8, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER, default='male')
    city = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    safe_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, default=[], related_name='safe_users'
    )


class Invite(models.Model):
    """ Invite's model between users
    """
    from_user = models.ForeignKey(SecureUser, on_delete=models.PROTECT, related_name='from_user', unique=False)
    to_user = models.ForeignKey(SecureUser, on_delete=models.PROTECT, related_name='to_user', unique=False)

    def __str__(self):
        return f'Invite from {self.from_user} to {self.to_user}'
