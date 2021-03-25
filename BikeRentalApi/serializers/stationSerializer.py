from BikeRentalApi.models import BikeStation
from rest_framework import serializers


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeStation
        exclude = ['state']
