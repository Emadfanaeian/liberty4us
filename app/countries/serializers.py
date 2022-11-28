"""countries serializer"""
from core.models import Countries
from rest_framework import serializers


class CountryStatesSerializer(serializers.ModelSerializer):
    """Serializer for Country States"""


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for countries"""
    class Meta:
        """ meta """
        model = Countries
        fields = ('id', 'name', )
        read_only_fields = ('id', )
