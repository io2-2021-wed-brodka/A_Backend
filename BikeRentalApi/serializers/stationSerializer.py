from rest_framework.fields import SerializerMethodField

from BikeRentalApi.enums import BikeState
from BikeRentalApi.models import BikeStation, Bike
from rest_framework import serializers


class StationSerializer(serializers.ModelSerializer):
    status = SerializerMethodField()
    activeBikesCount = SerializerMethodField()

    class Meta:
        model = BikeStation
        exclude = ['state']

    def get_status(self, obj: BikeStation):
        return obj.state.label

    def get_activeBikesCount(self, obj: BikeStation):
        return Bike.objects.filter(station__pk = obj.pk, bike_state = BikeState.Working).count()
