from django.http import JsonResponse
from rest_framework import status

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role
from BikeRentalApi.models import Malfunction
from BikeRentalApi.serializers.malfunctionSerializer import MalfunctionSerializer

# GET: list all malfunctions


@RoleRequired([Role.Tech, Role.Admin])
def get(request):
    malfunctions = Malfunction.objects.all()
    serializer = MalfunctionSerializer(malfunctions, many = True)

    return JsonResponse(
        {"malfunctions": serializer.data},
        safe = False,
        status = status.HTTP_200_OK
    )
