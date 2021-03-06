import io

from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from BikeRentalApi.models import Bike
from BikeRentalApi.serializers.addBikeToTheStationSerializer import AddBikeStationSerializer
from BikeRentalApi.serializers.bikeSerializer import BikeSerializer
from BikeRentalApi.enums import Role, BikeState
from BikeRentalApi.decorators.roleRequired import RoleRequired

# POST: create bikes
# GET: list all bikes


@RoleRequired([Role.Tech, Role.Admin])
def get(request):
    bikes = Bike.objects.all()
    serializer = BikeSerializer(bikes, many = True)

    return JsonResponse(
        {"bikes": serializer.data},
        safe = False,
        status = status.HTTP_200_OK
    )


@RoleRequired([Role.Admin])
def post(request):
    stream = io.BytesIO(request.body)
    serializer = AddBikeStationSerializer(data = JSONParser().parse(stream))

    if not serializer.is_valid():
        return HttpResponse(status = status.HTTP_400_BAD_REQUEST)

    station = serializer.create(serializer.validated_data)

    if station is None:
        return HttpResponse(status = status.HTTP_404_NOT_FOUND)

    if Bike.objects.filter(station_id__exact = station.pk).count() >= station.bikes_limit:
        return JsonResponse(
            {"message": "Cannot add a new bike to this station"},
            status = status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    bike = Bike.objects.create(station = station, bike_state = BikeState.Working)

    return JsonResponse(
        BikeSerializer(bike).data,
        safe = False,
        status = status.HTTP_201_CREATED
    )
