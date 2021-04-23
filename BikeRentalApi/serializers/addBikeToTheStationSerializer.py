from rest_framework import serializers
from rest_framework.fields import IntegerField

from BikeRentalApi.models import BikeStation


class AddBikeStationSerializer(serializers.ModelSerializer):
    stationId = IntegerField()

    class Meta:
        model = BikeStation
        fields = ['stationId']

    def create(self, validated_data):
        try:
            return BikeStation.objects.get(id = validated_data['stationId'])
        except BikeStation.DoesNotExist:
            return None
