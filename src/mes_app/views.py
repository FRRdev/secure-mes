from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from src.mes_app.models import Message, CurrentKey
from src.mes_app.serializers import MessageCreateSerializer, GetMessageSerializer
from src.neuro_base.service import encode_message


@api_view(["POST"])
def create_message(request, pk):
    mes_serializer = MessageCreateSerializer(data=request.data)
    mes_serializer.is_valid(raise_exception=True)
    q = (Q(first_user=request.user) & Q(second_user=pk)) | (
            Q(first_user=pk) & Q(second_user=request.user))
    ck = get_object_or_404(CurrentKey, q)
    content = encode_message(mes_serializer.validated_data['text'], ck.key.value)
    mes = Message.objects.create(sender=request.user, recipient_id=pk, content=content, key=ck.key)
    serializer = GetMessageSerializer(instance=mes)
    return Response(serializer.data, status=status.HTTP_200_OK)
