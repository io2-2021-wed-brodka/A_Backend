from rest_framework import serializers
from rest_framework.fields import CharField, DateTimeField

from BikeRentalApi.models import Reservation
from .stationSerializer import StationSerializer


class ReservationSerializer(serializers.ModelSerializer):
    id = CharField(source = 'bike.id')
    station = StationSerializer(many = False, read_only = True)
    reservedAt = DateTimeField(source = 'start_date')
    reservedTill = DateTimeField(source = 'expire_date')

    class Meta:
        model = Reservation
        fields = ['id', 'station', 'reservedAt', 'reservedTill']
