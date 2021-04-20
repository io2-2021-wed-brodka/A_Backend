from rest_framework import serializers
from rest_framework.fields import IntegerField

from BikeRentalApi.models import BikeStation


class AddBikeStationSerializer(serializers.ModelSerializer):
    id = IntegerField()

    class Meta:
        model = BikeStation
        fields = ['id']

    def create(self, validated_data):
        try:
            return BikeStation.objects.get(id = validated_data['id'])
        except BikeStation.DoesNotExist:
            return None
