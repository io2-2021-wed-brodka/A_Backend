from rest_framework import serializers
from rest_framework.fields import IntegerField

from BikeRentalApi.models import Bike


class RentBikeSerializer(serializers.ModelSerializer):
    id = IntegerField()

    class Meta:
        model = Bike
        fields = ['id']

    def create(self, validated_data):
        return Bike.objects.get(id = validated_data['id'])
