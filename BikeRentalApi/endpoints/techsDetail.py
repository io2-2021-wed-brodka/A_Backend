from django.http import JsonResponse
from rest_framework import status

from BikeRentalApi.enums import Role
from BikeRentalApi.models import Tech
from BikeRentalApi.serializers.userSerializer import UserSerializer


def delete(user, pk):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_401_UNAUTHORIZED)

    tech = Tech.objects.filter(pk = pk).first()

    if tech is None:
        return JsonResponse({"message": "Tech not found"}, status = status.HTTP_404_NOT_FOUND)

    data = UserSerializer(tech).data
    Tech.delete(tech)

    return JsonResponse(data, safe = False, status = status.HTTP_200_OK)


def get(user, pk):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_401_UNAUTHORIZED)

    tech = Tech.objects.filter(pk = pk).first()

    if tech is None:
        return JsonResponse({"message": "Tech not found"}, status = status.HTTP_404_NOT_FOUND)

    data = UserSerializer(tech).data

    return JsonResponse(data, safe = False, status = status.HTTP_200_OK)
