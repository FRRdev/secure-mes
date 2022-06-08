from rest_framework.decorators import action
from rest_framework.response import Response

from src.profiles.serializers import GetShorUserInfoSerializer
from . import services


class LikedMixin:
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        """ Like to `obj`.
        """
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(methods=['POST'], detail=True)
    def unlike(self, request, pk=None):
        """ Remove like from `obj`.
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()

    @action(methods=['GET'], detail=True)
    def fans(self, request, pk=None):
        """ et all users who have liked `obj`
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = GetShorUserInfoSerializer(fans, many=True)
        return Response(serializer.data)
