from rest_framework import serializers
from .models import Post
from . import services

from src.profiles.serializers import GetShorUserInfoSerializer


class PostSerializer(serializers.ModelSerializer):
    """ Post Serializers for create/list/update actions
    """
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'allowed_users',
            'is_fan',
            'total_likes',
        )

    def get_is_fan(self, obj) -> bool:
        """ Checks whether the user has liked `obj`.
        """
        user = self.context.get('request').user
        return services.is_fan(obj, user)


class DetailPostSerializer(PostSerializer):
    """ Post serializer for retrieve action
    """
    allowed_users = GetShorUserInfoSerializer(many=True)
    likes = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'allowed_users',
            'is_fan',
            'total_likes',
            'likes'
        )
