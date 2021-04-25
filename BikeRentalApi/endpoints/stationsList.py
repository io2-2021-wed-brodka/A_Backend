import io

from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from BikeRentalApi.models import BikeStation
from BikeRentalApi.serializers.addStationSerializer import AddStationSerializer
from BikeRentalApi.serializers.stationSerializer import StationSerializer
from BikeRentalApi.enums import Role


def get():
    stations = BikeStation.objects.all()
    serializer = StationSerializer(stations, many = True)

    return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)


def post(request, user):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_403_FORBIDDEN)

    stream = io.BytesIO(request.body)
    data = JSONParser().parse(stream)
    serializer = AddStationSerializer(data = data)

    if not serializer.is_valid():
        return JsonResponse({}, status = status.HTTP_400_BAD_REQUEST)

    station = serializer.save()

    return JsonResponse(StationSerializer(station).data, safe = False, status = status.HTTP_201_CREATED)
