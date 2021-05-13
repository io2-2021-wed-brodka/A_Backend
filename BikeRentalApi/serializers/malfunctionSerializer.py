from rest_framework import serializers
from rest_framework.fields import CharField

from BikeRentalApi.models import Malfunction


class MalfunctionSerializer(serializers.ModelSerializer):
    id = CharField()
    bikeId = CharField(source = 'bike.id')
    reportingUserId = CharField(source = 'reporting_user.id')

    class Meta:
        model = Malfunction
        exclude = ['state', 'bike', 'reporting_user']
