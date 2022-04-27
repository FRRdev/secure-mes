from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/", views.create_message, name="create_message"),
]
