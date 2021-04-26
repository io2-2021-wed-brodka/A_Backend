from django.http import JsonResponse
from rest_framework import status

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role, StationState
from BikeRentalApi.models import BikeStation
from BikeRentalApi.serializers.stationSerializer import StationSerializer

# GET: list working stations


@RoleRequired([Role.Admin])
def get(request):
    stations = BikeStation.objects.filter(state = StationState.Working)
    serializer = StationSerializer(stations, many = True)

    return JsonResponse(
        serializer.data,
        safe = False,
        status = status.HTTP_200_OK
    )
