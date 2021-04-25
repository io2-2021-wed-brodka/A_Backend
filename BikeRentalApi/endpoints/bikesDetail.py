from django.http import JsonResponse, HttpResponse
from rest_framework import status

from BikeRentalApi.enums import Role, BikeState
from BikeRentalApi.models import Bike

# DELETE: delete a bike


def delete(user, pk):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_403_FORBIDDEN)

    bike = Bike.objects.filter(pk = pk).first()

    if bike is None:
        return JsonResponse({"message": "Bike not found"}, status = status.HTTP_404_NOT_FOUND)
    if bike.bike_state != BikeState.Blocked:
        return JsonResponse({"message": "Bike is not blocked"}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

    bike.delete()

    return HttpResponse(status = status.HTTP_204_NO_CONTENT)
