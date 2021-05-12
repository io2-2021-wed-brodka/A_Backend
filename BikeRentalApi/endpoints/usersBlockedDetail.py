from django.http import JsonResponse, HttpResponse
from rest_framework import status

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role, UserState
from BikeRentalApi.models import AppUser


@RoleRequired([Role.Admin])
def delete(request, pk):
    try:
        user = AppUser.objects.get(pk = pk)
    except AppUser.DoesNotExist:
        return JsonResponse(
            {"message": "User not found"},
            status = status.HTTP_404_NOT_FOUND
        )

    if user.state == UserState.Active:
        return JsonResponse(
            {"message": "User not blocked"},
            status = status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    user.state = UserState.Active
    user.save()

    return HttpResponse(status = status.HTTP_204_NO_CONTENT)
