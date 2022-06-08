from django.contrib.contenttypes.models import ContentType

from src.profiles.models import SecureUser
from .models import Like


def add_like(obj, user):
    """ Like to `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user
    )
    return like


def remove_like(obj, user):
    """ Remove like from `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()


def is_fan(obj, user) -> bool:
    """ Checks whether the user has liked `obj`.
    """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    )
    return likes.exists()


def get_fans(obj):
    """ Get all users who have liked `obj`
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return SecureUser.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id
    )
