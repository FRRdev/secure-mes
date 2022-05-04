from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/", views.create_message, name="create_message"),
    path("read/<int:pk>/", views.read_message, name="read_message"),
    path("update/<int:pk>/", views.EditMessageView.as_view(), name="edit_message"),
    path("refresh/<int:pk>/", views.ResetCurrentKeyView.as_view(), name="refresh_key"),
    path("send/list/", views.ListSendMessageView.as_view(), name="list_send_message"),
    path("receive/list/", views.ListReceiveMessageView.as_view(), name="list_receive_message"),
]
