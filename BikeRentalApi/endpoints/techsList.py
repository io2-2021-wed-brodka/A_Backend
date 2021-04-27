import io

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role
from BikeRentalApi.models import Tech
from BikeRentalApi.serializers.userSerializer import UserSerializer

# GET: list all techs
# POST: create a tech


@RoleRequired([Role.Admin])
def get(request):
    techs = Tech.objects.all()
    serializer = UserSerializer(techs, many = True)

    return JsonResponse(
        serializer.data,
        safe = False,
        status = status.HTTP_200_OK
    )


@RoleRequired([Role.Admin])
def post(request):
    stream = io.BytesIO(request.body)
    data = JSONParser().parse(stream)

    try:
        username = data['name']
        password = data['password']
    except KeyError:
        return JsonResponse(
            {"message": "Bad data"},
            status = status.HTTP_400_BAD_REQUEST
        )

    try:
        User.objects.get(username = username)
        return JsonResponse(
            {'message': 'Conflicting registration data'},
            status = status.HTTP_409_CONFLICT
        )
    except User.DoesNotExist:
        user = User.objects.create_user(username, f'{username}@bikes.com', password)
        tech = Tech.objects.create(user = user)

        return JsonResponse(
            UserSerializer(tech).data,
            safe = False,
            status = status.HTTP_200_OK
        )
