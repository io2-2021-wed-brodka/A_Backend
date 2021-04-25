import io

from django.http import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework import status

from BikeRentalApi.models import Bike, BikeStation, BikeState, Rental
from BikeRentalApi.serializers.bikeSerializer import BikeSerializer
from BikeRentalApi.serializers.rentBikeSerializer import RentBikeSerializer

# GET: list all bikes assigned to the given station
# POST: return a bike to the given station


def get(pk):
    bikes = Bike.objects.filter(station_id__exact = pk)
    serializer = BikeSerializer(bikes, many = True)
    return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)


def post(request, user, pk):
    stream = io.BytesIO(request.body)
    serializer = RentBikeSerializer(data = JSONParser().parse(stream))

    if not serializer.is_valid():
        return JsonResponse({}, status = status.HTTP_400_BAD_REQUEST)

    bike = serializer.create(serializer.validated_data)

    if bike is None:
        return JsonResponse({"message": "Bike not found"}, status = status.HTTP_404_NOT_FOUND)

    station = BikeStation.objects.filter(pk = pk).first()

    if station is None:
        return JsonResponse({"message": "Station not found"}, status = status.HTTP_404_NOT_FOUND)

    rental = Rental.objects.filter(user = user, bike = bike)

    if rental.count() == 0:
        return JsonResponse(
            {'message': 'No user\'s rentals found for given bike.'},
            status = status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    rental.delete()

    bike.bike_state = BikeState.Working
    bike.station = station
    bike.save()

    serializer = BikeSerializer(bike)
    return JsonResponse(serializer.data, safe = False, status = status.HTTP_201_CREATED)
