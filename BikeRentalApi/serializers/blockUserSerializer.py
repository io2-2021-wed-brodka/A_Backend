from rest_framework import serializers
from rest_framework.fields import CharField

from BikeRentalApi.models import AppUser


class BlockUserSerializer(serializers.ModelSerializer):
    id = CharField()

    class Meta:
        model = AppUser
        fields = ['id']

    def create(self, validated_data):
        try:
            return AppUser.objects.get(id = int(validated_data['id']))
        except AppUser.DoesNotExist:
            return None
