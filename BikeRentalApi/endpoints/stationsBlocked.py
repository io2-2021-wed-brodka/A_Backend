import io

from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser

from BikeRentalApi.enums import Role, StationState
from BikeRentalApi.models import BikeStation
from BikeRentalApi.serializers.stationSerializer import StationSerializer

# GET: list all blocked stations
# POST: block station


def get(user):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Forbidden"}, status = status.HTTP_403_FORBIDDEN)
    stations = BikeStation.objects.filter(state = StationState.Blocked)
    serializer = StationSerializer(stations, many = True)

    return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)


def post(request, user):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Forbidden"}, status = status.HTTP_403_FORBIDDEN)

    stream = io.BytesIO(request.body)
    data = JSONParser().parse(stream)

    try:
        id = int(data['id'])
    except KeyError:
        return JsonResponse({"message": "Bad data"}, status = status.HTTP_400_BAD_REQUEST)

    try:
        station = BikeStation.objects.get(id = id)
    except BikeStation.DoesNotExist:
        return JsonResponse({"message": "Station not found"}, status = status.HTTP_404_NOT_FOUND)

    if station.state == StationState.Blocked:
        return JsonResponse({"message": "Station already blocked"},
                            status = status.HTTP_422_UNPROCESSABLE_ENTITY)

    station.state = StationState.Blocked
    station.save()

    return JsonResponse(StationSerializer(station).data, safe = False, status = status.HTTP_201_CREATED)
