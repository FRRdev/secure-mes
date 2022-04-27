from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.db.utils import IntegrityError

from .models import SecureUser, Invite
from .serializers import (
    CreateSecureUserSerializer,
    GetPublicSecureUserSerializer,
    ListSendInviteSerializer,
    ListReceiveInviteSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from src.base.classes import MixedPermission, CreateListDestroy, ListDestroy
from src.base.permissions import IsAuthor
from src.mes_app.service import generate_neuro_key


class SecureUserView(MixedPermission, ModelViewSet):
    """ CRUD Secure User
    """
    queryset = SecureUser.objects.all()
    serializer_class = CreateSecureUserSerializer
    permission_classes_by_action = {
        'list': [AllowAny],
        'create': [AllowAny],
        'update': [IsAuthor],
        'destroy': [IsAuthenticated]
    }

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return GetPublicSecureUserSerializer
        return CreateSecureUserSerializer

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        password_hash = make_password(password)
        serializer.validated_data['password'] = password_hash
        serializer.save()


class InviteSendView(CreateListDestroy):
    """ Create List Destroy view to send Invite
    """
    serializer_class = ListSendInviteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Invite.objects.filter(from_user=self.request.user)

    def create(self, request, *args, **kwargs):
        q = (Q(from_user=request.user) & Q(to_user=kwargs['pk'])) | (
                Q(from_user=kwargs['pk']) & Q(to_user=request.user))
        if Invite.objects.filter(q).exists():
            return Response({'error': 'Invite already exists'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.pk == kwargs['pk']:
            return Response({'error': 'You can not invite yourself'}, status=status.HTTP_404_NOT_FOUND)
        try:
            Invite.objects.create(from_user_id=self.request.user.pk, to_user_id=kwargs['pk'])
        except IntegrityError:
            return Response({'error': 'Incorrect data to send invite'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'created successfully'}, status=status.HTTP_201_CREATED)


class InviteReceiveView(ListDestroy):
    """ List and Destroy view to received invites
    """
    serializer_class = ListReceiveInviteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Invite.objects.filter(to_user=self.request.user)


class InviteAcceptView(APIView):
    """ Accept offer and Add into friend
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            _invite = Invite.objects.select_related('from_user').get(pk=pk, to_user=request.user)
        except Invite.DoesNotExist:
            return Response({'error': 'Invite does not exist'}, status=status.HTTP_404_NOT_FOUND)
        _from_user = _invite.from_user
        _user = SecureUser.objects.get(pk=request.user.pk)
        _user.safe_user.add(_from_user)
        _user.save()
        _from_user.safe_user.add(_user)
        _from_user.save()
        _invite.delete()
        generate_neuro_key(_user, _from_user)
        return Response({'msg': 'User added successfully'}, status=status.HTTP_201_CREATED)


class DeleteFriendView(APIView):
    """ Delete friend
    """
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        current_user = SecureUser.objects.get(pk=request.user.pk)
        delete_user = get_object_or_404(SecureUser, pk=pk)
        current_user.safe_user.remove(delete_user)
        delete_user.safe_user.remove(current_user)
        current_user.save()
        delete_user.save()
        return Response({'msg': 'User deleted successfully'}, status=status.HTTP_200_OK)
