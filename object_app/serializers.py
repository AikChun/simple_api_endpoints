from .models import GenericObject
from rest_framework import serializers

class GenericObjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = GenericObject
        fields = ('mykey', 'value', 'created_at')
