import io

from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from BikeRentalApi.models import Bike
from BikeRentalApi.serializers.bikeSerializer import BikeSerializer
from BikeRentalApi.enums import Role, BikeState


def get(user):
    if user.role < Role.Tech:
        return JsonResponse({"message": "Forbidden"}, status = status.HTTP_403_FORBIDDEN)

    bikes = Bike.objects.filter(bike_state = BikeState.Blocked)
    serializer = BikeSerializer(bikes, many = True)

    return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)


def post(request, user):
    if user.role < Role.Tech:
        return JsonResponse({"message": "Forbidden"}, status = status.HTTP_403_FORBIDDEN)

    stream = io.BytesIO(request.body)
    data = JSONParser().parse(stream)

    try:
        id = int(data['id'])
    except KeyError:
        return JsonResponse({"message": "Bad data"}, status = status.HTTP_400_BAD_REQUEST)

    bike = Bike.objects.filter(id = id).first()

    if bike is None:
        return JsonResponse({"message": "Bike not found"}, status = status.HTTP_404_NOT_FOUND)

    if bike.bike_state == BikeState.Blocked or bike.bike_state == BikeState.InService:
        return JsonResponse({"message": "Bike already blocked or rented"},
                            status = status.HTTP_422_UNPROCESSABLE_ENTITY)
    bike.bike_state = BikeState.Blocked
    bike.save()

    return JsonResponse(BikeSerializer(bike).data, safe = False, status = status.HTTP_201_CREATED)
