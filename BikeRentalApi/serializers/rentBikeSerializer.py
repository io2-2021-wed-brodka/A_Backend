from rest_framework import serializers
from rest_framework.fields import CharField

from BikeRentalApi.models import Bike


class RentBikeSerializer(serializers.ModelSerializer):
    id = CharField()

    class Meta:
        model = Bike
        fields = ['id']

    def create(self, validated_data):
        try:
            return Bike.objects.get(id = int(validated_data['id']))
        except Bike.DoesNotExist:
            return None
