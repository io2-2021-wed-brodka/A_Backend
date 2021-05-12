from django.http import JsonResponse
from rest_framework import status

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role, StationState
from BikeRentalApi.models import BikeStation
from BikeRentalApi.serializers.stationSerializer import StationSerializer

# GET: list working stations


@RoleRequired([Role.User, Role.Tech, Role.Admin])
def get(request):
    stations = BikeStation.objects.filter(state = StationState.Working)
    serializer = StationSerializer(stations, many = True)

    return JsonResponse(
        {"stations": serializer.data},
        safe = False,
        status = status.HTTP_200_OK
    )
