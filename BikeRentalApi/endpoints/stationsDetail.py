from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.models import Bike, BikeStation
from BikeRentalApi.serializers.stationSerializer import StationSerializer
from BikeRentalApi.enums import Role, StationState

# GET: get the details of the given station
# DELETE: delete the given station


@RoleRequired([Role.User, Role.Tech, Role.Admin])
def get(request, pk):
    station = get_object_or_404(BikeStation, pk = pk)
    serializer = StationSerializer(station)

    return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)


@RoleRequired([Role.Admin])
def delete(request, pk):
    station = BikeStation.objects.filter(pk = pk).first()

    if station is None:
        return JsonResponse({"message": "Station not found"}, status = status.HTTP_404_NOT_FOUND)

    if station.state != StationState.Blocked:
        return JsonResponse({'message': 'Station is not in blocked state'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

    if Bike.objects.filter(station_id__exact = station.pk).count() > 0:
        return JsonResponse({'message': 'Station is not empty'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

    station.delete()

    return HttpResponse(status = status.HTTP_204_NO_CONTENT)
