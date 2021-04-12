from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField

from BikeRentalApi.models import AppUser


class UserSerializer(serializers.ModelSerializer):
    id = IntegerField(label = 'ID', read_only = True)
    name = SerializerMethodField()

    class Meta:
        model = AppUser
        fields = ['name', 'id']

    def get_name(self, obj):
        return obj.user.first_name
