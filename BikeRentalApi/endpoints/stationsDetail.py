from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status

from BikeRentalApi.models import Bike, BikeStation
from BikeRentalApi.serializers.stationSerializer import StationSerializer
from BikeRentalApi.enums import Role, StationState


def get(pk):
    station = get_object_or_404(BikeStation, pk = pk)
    serializer = StationSerializer(station)

    return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)


def delete(user, pk):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_403_FORBIDDEN)

    station = BikeStation.objects.filter(pk = pk).first()

    if station is None:
        return JsonResponse({"message": "Station not found"}, status = status.HTTP_404_NOT_FOUND)

    if station.state != StationState.Blocked:
        return JsonResponse({'message': 'Station is not in blocked state'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

    if Bike.objects.filter(station_id__exact = station.pk).count() > 0:
        return JsonResponse({'message': 'Station is not empty'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

    data = StationSerializer(station).data
    station.delete()

    return JsonResponse(data, safe = False, status = status.HTTP_200_OK)
