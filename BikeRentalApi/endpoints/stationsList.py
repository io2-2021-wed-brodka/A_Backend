import io

from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.models import BikeStation
from BikeRentalApi.serializers.addStationSerializer import AddStationSerializer
from BikeRentalApi.serializers.stationSerializer import StationSerializer
from BikeRentalApi.enums import Role

# GET: list all stations
# POST: add new station


@RoleRequired([Role.Tech, Role.Admin])
def get(request):
    stations = BikeStation.objects.all()
    serializer = StationSerializer(stations, many = True)

    return JsonResponse(
        {"stations": serializer.data},
        safe = False,
        status = status.HTTP_200_OK
    )


@RoleRequired([Role.Admin])
def post(request):
    stream = io.BytesIO(request.body)
    data = JSONParser().parse(stream)
    serializer = AddStationSerializer(data = data)

    if not serializer.is_valid():
        return HttpResponse(status = status.HTTP_400_BAD_REQUEST)

    station = serializer.save()

    return JsonResponse(
        StationSerializer(station).data,
        safe = False,
        status = status.HTTP_201_CREATED
    )
