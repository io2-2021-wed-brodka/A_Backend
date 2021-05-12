import io

from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.parsers import JSONParser

from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role, UserState
from BikeRentalApi.models import AppUser
from BikeRentalApi.serializers.userSerializer import UserSerializer
from BikeRentalApi.serializers.blockUserSerializer import BlockUserSerializer


@RoleRequired([Role.Admin])
def get(request):
    users = AppUser.objects.filter(state = UserState.Banned)
    serializer = UserSerializer(users, many = True)

    return JsonResponse(
        {"users": serializer.data},
        safe = False,
        status = status.HTTP_200_OK
    )


@RoleRequired([Role.Admin])
def post(request):
    stream = io.BytesIO(request.body)
    data = JSONParser().parse(stream)

    serializer = BlockUserSerializer(data = data)

    if not serializer.is_valid():
        return HttpResponse(status = status.HTTP_400_BAD_REQUEST)

    user = serializer.create(serializer.validated_data)

    if user is None:
        return JsonResponse(
            {'message': 'User not found'},
            status = status.HTTP_404_NOT_FOUND
        )

    if user.state == UserState.Banned:
        return JsonResponse(
            {'message': 'User already blocked'},
            status = status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    user.state = UserState.Banned
    user.save()

    return JsonResponse(
        UserSerializer(user).data,
        status = status.HTTP_201_CREATED
    )
