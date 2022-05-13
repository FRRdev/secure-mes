from rest_framework import serializers

from src.mes_app.models import Message
from src.profiles.serializers import GetPublicMessageUserSerializer, GetShorUserInfoSerializer


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


class GetUserForStatisticSerializer(serializers.Serializer):
    """ Serializer for user for statistic
    """
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(max_length=150, allow_null=True, allow_blank=True)
    email = serializers.EmailField()
    cnt = serializers.IntegerField()


class GetStatisticSerializer(serializers.Serializer):
    """ Serializer for statistic for messages
    """
    total_count_messages = serializers.IntegerField()
    top_users = GetUserForStatisticSerializer(many=True)
