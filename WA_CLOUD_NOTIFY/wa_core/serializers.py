# serializers.py
from rest_framework import serializers

class SendMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    recipient_id = serializers.CharField()
    recipient_type = serializers.CharField(default="individual")
    preview_url = serializers.BooleanField(default=True)


