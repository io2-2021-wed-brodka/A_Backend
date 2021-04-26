from django.http import JsonResponse, HttpResponse
from rest_framework import status

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role, StationState
from BikeRentalApi.models import BikeStation

# DELETE: unblock the given station


@RoleRequired([Role.Admin])
def delete(request, pk):
    try:
        station = BikeStation.objects.get(id = pk)
    except BikeStation.DoesNotExist:
        return JsonResponse({"message": "Station not found"}, status = status.HTTP_404_NOT_FOUND)

    if station is None:
        return JsonResponse({"message": "Station not found"}, status = status.HTTP_404_NOT_FOUND)

    if station.state != StationState.Blocked:
        return JsonResponse({"message": "Station not blocked"}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

    station.state = StationState.Working
    station.save()

    return HttpResponse(status = status.HTTP_204_NO_CONTENT)
