from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView

from src.mes_app.service import refresh_neuro_key
from src.neuro_base.service import encode_message, decode_message
from src.mes_app.models import Message, CurrentKey
from src.mes_app.serializers import (
    MessageCreateReadSerializer,
    GetMessageSendSerializer,
    GetMessageReceiveSerializer,
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_message(request, pk):
    """ Create message by user's pk
    """
    mes_serializer = MessageCreateReadSerializer(data=request.data)
    mes_serializer.is_valid(raise_exception=True)
    q = (Q(first_user=request.user) & Q(second_user=pk)) | (
            Q(first_user=pk) & Q(second_user=request.user))
    ck = get_object_or_404(CurrentKey, q)
    content = encode_message(mes_serializer.validated_data['text'], ck.key.value)
    mes = Message.objects.create(sender=request.user, recipient_id=pk, content=content, key=ck.key)
    serializer = GetMessageSendSerializer(instance=mes)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@cache_page(60 * 15)
def read_message(request, pk):
    """ Read message by message's pk
    """
    q = (Q(sender=request.user) | Q(recipient=request.user)) & Q(pk=pk)
    mes = get_object_or_404(Message, q)
    text = decode_message(mes.content, mes.key.value)
    data = {"text": text}
    serializer = MessageCreateReadSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class EditMessageView(APIView):
    """ Change flag is active for message
    """
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        mes = get_object_or_404(Message, pk=pk, recipient=self.request.user)
        mes.is_active = False
        mes.save()
        serializer = GetMessageReceiveSerializer(mes)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListSendMessageView(ListAPIView):
    """ Get a list of sent messages
    """
    serializer_class = GetMessageSendSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)


class ListReceiveMessageView(ListAPIView):
    """ Get a list of received messages
    """
    serializer_class = GetMessageReceiveSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user)


class ResetCurrentKeyView(APIView):
    """ Reset neuro key
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        q = (Q(first_user=request.user) & Q(second_user=pk)) | (
                Q(first_user=pk) & Q(second_user=request.user))
        ck = get_object_or_404(CurrentKey, q)
        refresh_neuro_key(ck)
        return Response({'msg': 'Key refreshed successfully'}, status=status.HTTP_200_OK)
