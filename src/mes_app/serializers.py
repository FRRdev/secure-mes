from rest_framework import serializers

from src.mes_app.models import Message
from src.profiles.serializers import GetPublicMessageUserSerializer


class MessageCreateReadSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=5000)


class GetMessageSendSerializer(serializers.ModelSerializer):
    """ Serializer for sent messages
    """
    recipient = GetPublicMessageUserSerializer()

    class Meta:
        model = Message
        exclude = ('key', 'sender')


class GetMessageReceiveSerializer(serializers.ModelSerializer):
    """ Serializer for received messages
    """
    sender = GetPublicMessageUserSerializer()

    class Meta:
        model = Message
        exclude = ('key', 'recipient')
