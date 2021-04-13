from django.http import JsonResponse
from rest_framework import status

from BikeRentalApi.models import Bike
from BikeRentalApi.serializers.bikeSerializer import BikeSerializer
from BikeRentalApi.enums import Role


def delete(user, pk):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_401_UNAUTHORIZED)

    bike = Bike.objects.filter(pk = pk).first()

    if bike is None:
        return JsonResponse({"message": "Bike not found"}, status = status.HTTP_404_NOT_FOUND)

    data = BikeSerializer(bike).data
    bike.delete()

    return JsonResponse(data, safe = False, status = status.HTTP_200_OK)
