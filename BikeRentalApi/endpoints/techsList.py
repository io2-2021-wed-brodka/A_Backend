import io

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser

from BikeRentalApi.enums import Role
from BikeRentalApi.models import Tech
from BikeRentalApi.serializers.userSerializer import UserSerializer


def get(user):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_401_UNAUTHORIZED)

    techs = Tech.objects.all()
    serializer = UserSerializer(techs, many = True)

    return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)


def post(request, user):
    if user.role != Role.Admin:
        return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_401_UNAUTHORIZED)

    stream = io.BytesIO(request.body)
    data = JSONParser().parse(stream)

    try:
        username = data['name']
        password = data['password']
    except KeyError:
        return JsonResponse({"message": "Bad data"}, status = status.HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(username = username)
        return JsonResponse(status = 409, data = {'message': 'Conflicting registration data'})
    except User.DoesNotExist:
        user = User.objects.create_user(username, f'{username}@bikes.com', password)
        tech = Tech.objects.create(user = user)
        return JsonResponse({'id': tech.pk, 'name': tech.user.username})
