from rest_framework import serializers

from documents.serializers import DocumentSerializer
from properties.models import Property


class PropertySerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True)

    class Meta:
        model = Property
        exclude = ['user', 'local_node']
