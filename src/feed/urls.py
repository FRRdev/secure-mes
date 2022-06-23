from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentsView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
                  path('comment/', CommentsView.as_view({'post': 'create'})),
                  path('comment/<int:pk>/', CommentsView.as_view({'put': 'update', 'delete': 'destroy'})),
              ] + router.urls
