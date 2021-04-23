from django.http import JsonResponse
from rest_framework import status

from BikeRentalApi.enums import Role, StationState
from BikeRentalApi.models import BikeStation
from BikeRentalApi.serializers.stationSerializer import StationSerializer


def get(user):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Forbidden"}, status = status.HTTP_403_FORBIDDEN)
    stations = BikeStation.objects.filter(state = StationState.Working)
    serializer = StationSerializer(stations, many = True)

    return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)
