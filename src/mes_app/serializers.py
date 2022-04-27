from rest_framework import serializers

from src.mes_app.models import Message


class MessageCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=5000)


class GetMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('__all__')
