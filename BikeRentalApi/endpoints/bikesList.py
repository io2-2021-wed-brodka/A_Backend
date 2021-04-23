import io

from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from BikeRentalApi.models import Bike
from BikeRentalApi.serializers.addBikeToTheStationSerializer import AddBikeStationSerializer
from BikeRentalApi.serializers.bikeSerializer import BikeSerializer
from BikeRentalApi.enums import Role, BikeState


def get(user):
    if user.role < Role.Tech:
        return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_403_FORBIDDEN)

    bikes = Bike.objects.all()
    serializer = BikeSerializer(bikes, many = True)

    return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)


def post(request, user):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_403_FORBIDDEN)

    stream = io.BytesIO(request.body)
    serializer = AddBikeStationSerializer(data = JSONParser().parse(stream))

    if not serializer.is_valid():
        return JsonResponse({}, status = status.HTTP_400_BAD_REQUEST)

    station = serializer.create(serializer.validated_data)

    if station is None:
        return JsonResponse({}, status = status.HTTP_404_NOT_FOUND)

    bike = Bike()
    bike.bike_state = BikeState.Working
    bike.station = station
    bike.save()

    return JsonResponse(BikeSerializer(bike).data, safe = False, status = status.HTTP_201_CREATED)
