from django.db import models

from src.profiles.models import SecureUser


class Key(models.Model):
    """ Key model for encoding and decoding
    """
    value = models.CharField(max_length=100, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)


class CurrentKey(models.Model):
    """ Model current key between two users
    """
    first_user = models.ForeignKey(SecureUser, on_delete=models.CASCADE, related_name='ck_first_user')
    second_user = models.ForeignKey(SecureUser, on_delete=models.CASCADE, related_name='ck_second_user')
    key = models.OneToOneField(Key, on_delete=models.SET_NULL, null=True, related_name='current_data')


class Message(models.Model):
    """ Model of message
    """
    sender = models.ForeignKey(SecureUser, on_delete=models.CASCADE, related_name='sender_mes')
    recipient = models.ForeignKey(SecureUser, on_delete=models.CASCADE, related_name='recipient_mes')
    create_at = models.DateTimeField(auto_now_add=True)
    content = models.BinaryField()
    is_active = models.BooleanField(default=True)
    key = models.ForeignKey(Key, on_delete=models.SET_NULL, null=True, related_name='key_messages')