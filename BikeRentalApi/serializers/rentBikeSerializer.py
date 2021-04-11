from rest_framework import serializers

from BikeRentalApi.models import Bike


class RentBikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ['id']

    def create(self, validated_data):
        return Bike.objects.filter(**validated_data).first()
