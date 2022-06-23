from rest_framework import mixins, viewsets


class MixedPermission:
    """ Миксин permissions для action
    """

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class CreateListDestroy(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    """
    pass


class ListDestroy(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    """
    """
    pass


class CreateUpdateDestroy(mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          MixedPermission,
                          viewsets.GenericViewSet):
    """
    """
    pass
