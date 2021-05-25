from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, CharField, IntegerField

from BikeRentalApi.enums import BikeState
from BikeRentalApi.models import BikeStation


class StationSerializer(serializers.ModelSerializer):
    id = CharField()
    status = CharField(source = 'state.label')
    activeBikesCount = SerializerMethodField()
    bikesLimit = IntegerField(source = 'bikes_limit')

    class Meta:
        model = BikeStation
        exclude = ['state', 'bikes_limit']

    def get_activeBikesCount(self, obj: BikeStation):
        return obj.bike_set.filter(bike_state = BikeState.Working).count()

    def create(self, validated_data):
        if 'bikesLimit' in validated_data.keys():
            return BikeStation.objects.create(name = validated_data['name'], bikes_limit = validated_data['bikesLimit'])
        else:
            return BikeStation.objects.create(name = validated_data['name'])
