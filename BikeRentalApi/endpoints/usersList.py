from django.http import JsonResponse
from rest_framework import status

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role
from BikeRentalApi.models import AppUser
from BikeRentalApi.serializers.userSerializer import UserSerializer


@RoleRequired([Role.Admin])
def get(request):
    users = AppUser.objects.all()
    serializer = UserSerializer(users, many = True)

    return JsonResponse(
        {"users": serializer.data},
        safe = False,
        status = status.HTTP_200_OK
    )
