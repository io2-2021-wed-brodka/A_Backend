from rest_framework import serializers
from rest_framework.fields import IntegerField, ChoiceField, SerializerMethodField

from BikeRentalApi.enums import BikeState
from BikeRentalApi.models import Bike
from .stationSerializer import StationSerializer
from .userSerializer import UserSerializer


class BikeSerializer(serializers.ModelSerializer):
    id = IntegerField(label = 'ID', read_only = True)
    bike_state = ChoiceField(choices = BikeState, required = True)
    user = SerializerMethodField('get_user')
    station = StationSerializer(many = False, read_only = True)

    class Meta:
        model = Bike
        fields = '__all__'

    def get_user(self, obj):
        return UserSerializer(obj.rental_set.all().first().user).data if obj.rental_set.count() > 0 else None
