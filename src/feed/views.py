from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from src.base.permissions import IsAuthor
from .models import Post
from .serializers import PostSerializer, DetailPostSerializer
from .mixins import LikedMixin


@swagger_auto_schema(tags=["post"])
class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthor,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailPostSerializer
        return PostSerializer

    def get_permissions(self):
        if self.action == 'update':
            return [IsAuthor(), ]
        return [IsAuthenticated(), ]

    def get_queryset(self):
        return Post.objects.prefetch_related('likes', 'allowed_users').select_related('user').filter(
            Q(allowed_users__pk=self.request.user.pk) | Q(user=self.request.user),
            published=True
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
