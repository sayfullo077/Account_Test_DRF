from django.conf import settings
from rest_framework import serializers


class MediaURlSerializer(serializers.Serializer):
    def to_representation(self, obj):
        try:
            return self.context["request"].build_absolute_uri(obj.file.url)
        except Exception:
            return str(settings.HOST) + str(obj.file.url)