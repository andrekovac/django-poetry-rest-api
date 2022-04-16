from rest_framework import serializers
from .models import Show


class ShowSerializer(serializers.ModelSerializer):
    """ Serializer of a show """

    class Meta:
        model = Show
        fields = '__all__'
