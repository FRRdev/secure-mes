from rest_framework import serializers
from .models import Post, Comment
from . import services

from src.profiles.serializers import GetShorUserInfoSerializer


class BasePostSerializer(serializers.ModelSerializer):
    """ Post Serializers for all actions
    """
    is_fan = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True)

    def get_is_fan(self, obj) -> bool:
        """ Checks whether the user has liked `obj`.
        """
        user = self.context.get('request').user
        return services.is_fan(obj, user)


class ListPostSerializer(BasePostSerializer):
    """ Post Serializers for list actions
    """

    class Meta:
        model = Post
        fields = (
            'id',
            'allowed_users',
            'is_fan',
            'total_likes',
            'user'
        )


class PostSerializer(BasePostSerializer):
    """ Post Serializers for create/list/update actions
    """

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


class RecursiveSerializer(serializers.Serializer):
    """ Recursive get children
    """

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CreateCommentSerializer(serializers.ModelSerializer):
    """ Add comments to post
    """
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Comment
        fields = ("post", "text", "children")


class DetailPostSerializer(BasePostSerializer):
    """ Post serializer for retrieve action
    """
    allowed_users = GetShorUserInfoSerializer(many=True)
    comments = CreateCommentSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'allowed_users',
            'is_fan',
            'total_likes',
            'likes',
            'comments'
        )
