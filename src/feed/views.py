from django.db.models import Exists, OuterRef, Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post
from .serializers import PostSerializer
from .mixins import LikedMixin


@swagger_auto_schema(tags=["post"])
class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Post.objects.prefetch_related('likes').select_related('user').filter(
            Q(allowed_users__pk=self.request.user.pk) | Q(user=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
