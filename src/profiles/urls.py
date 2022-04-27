from django.urls import path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()

router.register(r'secureuser', views.SecureUserView, basename="secureuser")

urlpatterns = [
                  path("invite/send/", views.InviteSendView.as_view({'get': 'list'}), name="list_invite_send"),
                  path("invite/send/<int:pk>/", views.InviteSendView.as_view({'post': 'create', 'delete': 'destroy'}),
                       name="create_invite_send"),
                  path("invite/receive/", views.InviteReceiveView.as_view({'get': 'list'}), name="list_invite_receive"),
                  path("invite/receive/<int:pk>/", views.InviteReceiveView.as_view({'delete': 'destroy'}),
                       name="create_invite_receive"),
                  path("invite/receive/accept/<int:pk>/", views.InviteAcceptView.as_view(), name='accept_offer'),
                  path("friend/<int:pk>/", views.DeleteFriendView.as_view(), name='delete_friend'),
              ] + router.urls
