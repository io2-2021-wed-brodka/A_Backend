from django.http import JsonResponse, HttpResponse
from rest_framework import status

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.models import Bike
from BikeRentalApi.enums import Role, BikeState

# DELETE: unblock the given bike


@RoleRequired([Role.Tech, Role.Admin])
def delete(request, pk):
    bike = Bike.objects.filter(id = pk).first()
    if bike is None:
        return JsonResponse(
            {"message": "Bike not found"},
            status = status.HTTP_404_NOT_FOUND
        )

    if bike.bike_state != BikeState.Blocked:
        return JsonResponse(
            {"message": "Bike is not blocked"},
            status = status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    bike.bike_state = BikeState.Working
    bike.save()

    return HttpResponse(status = status.HTTP_204_NO_CONTENT)
