from rest_framework import permissions


class IsAuthor(permissions.IsAuthenticated):
    """ Permission to update User model
    """

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
