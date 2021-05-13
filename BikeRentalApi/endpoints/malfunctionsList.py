from django.http import JsonResponse
from rest_framework import status

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role
from BikeRentalApi.models import Malfunction
# POST: create bikes
# GET: list all bikes
from BikeRentalApi.serializers.malfunctionSerializer import MalfunctionSerializer


@RoleRequired([Role.Tech, Role.Admin])
def get(request):
    malfunctions = Malfunction.objects.all()
    serializer = MalfunctionSerializer(malfunctions, many = True)

    return JsonResponse(
        {"malfunctions": serializer.data},
        safe = False,
        status = status.HTTP_200_OK
    )
