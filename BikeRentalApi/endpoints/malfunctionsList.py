import io

from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.parsers import JSONParser

from BikeRentalApi.authentication import authenticate_bikes_user
from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role, BikeState
from BikeRentalApi.models import Malfunction, Bike, Rental
from BikeRentalApi.serializers.malfunctionSerializer import MalfunctionSerializer

# GET: list all malfunctions
# POST: report a malfunction


@RoleRequired([Role.Tech, Role.Admin])
def get(request):
    malfunctions = Malfunction.objects.all()
    serializer = MalfunctionSerializer(malfunctions, many = True)

    return JsonResponse(
        {"malfunctions": serializer.data},
        safe = False,
        status = status.HTTP_200_OK
    )


@RoleRequired([Role.User, Role.Tech, Role.Admin])
def post(request):
    user = authenticate_bikes_user(request)
    stream = io.BytesIO(request.body)
    data = JSONParser().parse(stream)

    try:
        id = int(data['id'])
        description = data['description']
    except KeyError or ValueError:
        return HttpResponse(status = status.HTTP_400_BAD_REQUEST)

    bike = Bike.objects.get(id = id)

    if bike is None:
        return JsonResponse(
            {'message': 'Bike not found'},
            status = status.HTTP_404_NOT_FOUND
        )

    try:
        rental = Rental.objects.get(bike_id = bike.id)
        if rental.user.id != user.id:
            raise ValueError
    except Rental.DoesNotExist or ValueError:
        return JsonResponse(
            {'message': 'Bike not rented by calling user'},
            status = status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    malfunction = Malfunction.objects.create(bike = bike, description = description, reporting_user = user.user)

    return JsonResponse(
        MalfunctionSerializer(malfunction).data,
        status = status.HTTP_201_CREATED
    )
