from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField

from BikeRentalApi.models import Bike
from .stationSerializer import StationSerializer
from .userSerializer import UserSerializer


class BikeSerializer(serializers.ModelSerializer):
    id = IntegerField(label = 'ID', read_only = True)
    status = SerializerMethodField()
    user = SerializerMethodField()
    station = StationSerializer(many = False, read_only = True)

    class Meta:
        model = Bike
        exclude = ['bike_state']

    def get_status(self, obj: Bike):
        return obj.bike_state.label

    def get_user(self, obj):
        return UserSerializer(obj.rental_set.all().first().user).data if obj.rental_set.count() > 0 else None
