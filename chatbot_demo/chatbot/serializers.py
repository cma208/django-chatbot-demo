from rest_framework import serializers
from .models import ChatMessage


class ChatRequestSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=True)
    doc_theme_name = serializers.CharField(max_length=255, required=True)
    max_context_messages = serializers.IntegerField(required=False)
    question = serializers.CharField(required=True)

class ChatMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'created_at', 'message', 'response']
