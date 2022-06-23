from rest_framework import permissions


class IsAuthor(permissions.IsAuthenticated):
    """ Permission to update Post model
    """

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id


class AllowedUser(permissions.IsAuthenticated):
    """ Permission to read Post
    """

    def has_object_permission(self, request, view, obj):
        return request.user.id in obj.allowed_users.values_list('id') \
               or obj.user.id == request.user.id
