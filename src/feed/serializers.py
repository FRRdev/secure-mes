from rest_framework import serializers
from .models import Post
from . import services


class PostSerializer(serializers.ModelSerializer):
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
