from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from rest_framework import status

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role
from BikeRentalApi.models import Tech
from BikeRentalApi.serializers.userSerializer import UserSerializer

# DELETE: delete a tech
# GET: get the details of the given tech


@RoleRequired([Role.Admin])
def delete(request, pk):
    try:
        tech = Tech.objects.get(pk = pk)
        Tech.delete(tech)
        User.objects.get(username = tech.user.username).delete()

        return HttpResponse(status = status.HTTP_204_NO_CONTENT)
    except Tech.DoesNotExist:
        return JsonResponse(
            {"message": "Tech not found"},
            status = status.HTTP_404_NOT_FOUND
        )


@RoleRequired([Role.Admin])
def get(request, pk):
    tech = Tech.objects.filter(pk = pk).first()

    if tech is None:
        return JsonResponse(
            {"message": "Tech not found"},
            status = status.HTTP_404_NOT_FOUND
        )

    data = UserSerializer(tech).data

    return JsonResponse(
        data,
        safe = False,
        status = status.HTTP_200_OK
    )
