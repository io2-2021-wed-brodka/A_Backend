from django.http import JsonResponse, HttpResponse
from rest_framework import status

from BikeRentalApi.enums import Role, StationState
from BikeRentalApi.models import BikeStation


def delete(user, pk):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Forbidden"}, status = status.HTTP_403_FORBIDDEN)
    station = BikeStation.objects.filter(pk = pk).first()

    if station is None:
        return JsonResponse({"message": "Station not found"}, status = status.HTTP_404_NOT_FOUND)

    if station.state != StationState.Blocked:
        return JsonResponse({"message": "Station not blocked"}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

    station.state = StationState.Working
    station.save()

    return HttpResponse(status = status.HTTP_204_NO_CONTENT)
