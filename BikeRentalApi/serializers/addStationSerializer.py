from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField

from BikeRentalApi.models import BikeStation


class AddStationSerializer(serializers.Serializer):
    name = CharField()
    bikesLimit = IntegerField(required = False)

    def create(self, validated_data):
        if 'bikesLimit' in validated_data.keys():
            return BikeStation.objects.create(name = validated_data['name'], bikes_limit = validated_data['bikesLimit'])
        else:
            return BikeStation.objects.create(name = validated_data['name'])
