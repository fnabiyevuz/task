from rest_framework import serializers


class SendSMSSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
    message = serializers.CharField(max_length=255)
