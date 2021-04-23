import io

from django.http import JsonResponse
from django.utils import timezone
from rest_framework.parsers import JSONParser
from rest_framework import status

from BikeRentalApi.models import Rental
from BikeRentalApi.serializers.bikeSerializer import BikeSerializer
from BikeRentalApi.serializers.rentBikeSerializer import RentBikeSerializer
from BikeRentalApi.enums import BikeState


def get(user):
    rentals = Rental.objects.filter(user_id__exact = user.pk)
    bikes = [rental.bike for rental in rentals]
    serializer = BikeSerializer(bikes, many = True)

    return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)


def post(request, user):
    stream = io.BytesIO(request.body)
    serializer = RentBikeSerializer(data = JSONParser().parse(stream))

    if not serializer.is_valid():
        return JsonResponse({}, status = status.HTTP_400_BAD_REQUEST)

    bike = serializer.create(serializer.validated_data)

    if bike is None:
        return JsonResponse({'message': 'Bike not found'}, status = status.HTTP_404_NOT_FOUND)

    if bike.bike_state == BikeState.InService:
        return JsonResponse({'message': 'Bike is already rented'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

    bike.bike_state = BikeState.InService
    bike.station = None
    bike.save()

    rental = Rental.objects.create(bike = bike, user = user, start_date = timezone.now())
    rental.save()

    serializer = BikeSerializer(bike)

    return JsonResponse(serializer.data, safe = False, status = status.HTTP_201_CREATED)
