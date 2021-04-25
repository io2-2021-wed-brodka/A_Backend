from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, CharField

from BikeRentalApi.enums import BikeState
from BikeRentalApi.models import BikeStation


class AddStationSerializer(serializers.Serializer):
    name = CharField()

    def create(self, validated_data):
        return BikeStation.objects.create(name = validated_data['name'])
