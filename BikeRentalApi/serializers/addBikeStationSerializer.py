from rest_framework import serializers

from BikeRentalApi.models import BikeStation


class AddBikeStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeStation
        fields = ['id']

    def create(self, validated_data):
        return BikeStation.objects.filter(**validated_data).first()
