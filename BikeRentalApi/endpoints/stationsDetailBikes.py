import io

from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.parsers import JSONParser

from BikeRentalApi.authentication import authenticate_bikes_user
from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role, StationState
from BikeRentalApi.models import Bike, BikeStation, BikeState, Rental
from BikeRentalApi.serializers.bikeSerializer import BikeSerializer
from BikeRentalApi.serializers.rentBikeSerializer import RentBikeSerializer


# GET: list all bikes assigned to the given station
# POST: return a bike to the given station


@RoleRequired([Role.User, Role.Tech, Role.Admin])
def get(request, pk):
    try:
        station = BikeStation.objects.get(pk = pk)
    except BikeStation.DoesNotExist:
        return JsonResponse(
            {"message": "Station not found"},
            status = status.HTTP_404_NOT_FOUND
        )
    user = authenticate_bikes_user(request)
    if station.state == StationState.Blocked and user.role == Role.User:
        return HttpResponse(status = status.HTTP_403_FORBIDDEN)
    bikes = Bike.objects.filter(station_id__exact = pk)
    serializer = BikeSerializer(bikes, many = True)
    return JsonResponse(
        serializer.data,
        safe = False,
        status = status.HTTP_200_OK
    )


@RoleRequired([Role.User, Role.Tech, Role.Admin])
def post(request, pk):
    user = authenticate_bikes_user(request)

    stream = io.BytesIO(request.body)
    serializer = RentBikeSerializer(data = JSONParser().parse(stream))

    if not serializer.is_valid():
        return HttpResponse(status = status.HTTP_400_BAD_REQUEST)

    bike = serializer.create(serializer.validated_data)

    if bike is None:
        return JsonResponse(
            {"message": "Bike not found"},
            status = status.HTTP_404_NOT_FOUND
        )

    station = BikeStation.objects.filter(pk = pk).first()

    if station is None:
        return JsonResponse(
            {"message": "Station not found"},
            status = status.HTTP_404_NOT_FOUND
        )

    rental = Rental.objects.filter(user = user, bike = bike)

    if rental.count() == 0:
        return JsonResponse(
            {"message": "No user's rentals found for given bike."},
            status = status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    rental.delete()

    bike.bike_state = BikeState.Working
    bike.station = station
    bike.save()

    serializer = BikeSerializer(bike)

    return JsonResponse(
        serializer.data,
        safe = False,
        status = status.HTTP_201_CREATED
    )
