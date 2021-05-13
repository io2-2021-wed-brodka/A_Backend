from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, CharField

from BikeRentalApi.enums import BikeState
from BikeRentalApi.models import BikeStation


class StationSerializer(serializers.ModelSerializer):
    id = CharField()
    status = CharField(source = 'state.label')
    activeBikesCount = SerializerMethodField()

    class Meta:
        model = BikeStation
        exclude = ['state']

    def get_activeBikesCount(self, obj: BikeStation):
        return obj.bike_set.filter(bike_state = BikeState.Working).count()

    def create(self, validated_data):
        return BikeStation.objects.create(name = validated_data['name'])
