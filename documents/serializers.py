from rest_framework import serializers

from documents.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['hash', 'size', 'created_at', 'content_type', 'name', 'contents', 'user']
        read_only_fields = ['user']
