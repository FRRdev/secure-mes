from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from src.base.permissions import IsAuthor, AllowedUser
from .models import Post, Comment
from .serializers import (
    PostSerializer,
    DetailPostSerializer,
    CreateCommentSerializer,
    ListPostSerializer
)

from .mixins import LikedMixin
from ..base.classes import CreateUpdateDestroy


@swagger_auto_schema(tags=["post"])
class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    """ Post CRUD View with likes
    """

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailPostSerializer
        elif self.action == 'list':
            return ListPostSerializer
        return PostSerializer

    def get_permissions(self):
        if self.action == 'update':
            return [IsAuthor(), ]
        elif self.action == 'retrieve':
            return [AllowedUser(), ]
        return [IsAuthenticated(), ]

    def get_queryset(self):
        return Post.objects.prefetch_related('likes', 'allowed_users','comments').select_related('user').filter(
            Q(allowed_users__pk=self.request.user.pk) | Q(user=self.request.user),
            published=True
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentsView(CreateUpdateDestroy):
    """ CRUD comments to posts
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes_by_action = {
        'create': [AllowedUser],
        'update': [AllowedUser],
        'destroy': [IsAuthor]
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
