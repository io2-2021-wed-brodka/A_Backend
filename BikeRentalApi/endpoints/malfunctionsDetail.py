from django.http import JsonResponse, HttpResponse
from rest_framework import status

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role
from BikeRentalApi.models import Malfunction


@RoleRequired([Role.Tech, Role.Admin])
def delete(request, pk):
    try:
        malfunction = Malfunction.objects.get(pk = pk)
    except Malfunction.DoesNotExist:
        return JsonResponse(
            {"message": "Station not found"},
            status = status.HTTP_404_NOT_FOUND
        )

    malfunction.delete()

    return HttpResponse(status = status.HTTP_204_NO_CONTENT)
