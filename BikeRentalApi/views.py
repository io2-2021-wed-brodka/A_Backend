from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import PermissionDenied, NotFound

from BikeRentalApi.models import Bike, Rental
from BikeRentalApi.serializers.bikeSerializer import BikeSerializer
from BikeRentalApi.authentication import authenticate
from BikeRentalApi.enums import Role


def bikes_list(request):
    user = authenticate(request)

    if request.method == 'GET':
        if user.role < Role.Tech:
            raise PermissionDenied()

        bikes = Bike.objects.all()
        serializer = BikeSerializer(bikes, many = True)
        return JsonResponse(serializer.data, safe = False, status = 200)
    elif request.method == 'POST':
        if user.role != Role.Admin:
            raise PermissionDenied()

        data = JSONParser().parse(request)
        serializer = BikeSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)

    raise NotFound()


def bikes_detail(request, pk):
    user = authenticate(request)

    if request.method == 'DELETE':
        if user.Role != Role.Admin:
            raise PermissionDenied()

        bike = get_object_or_404(Bike, pk = pk)
        serializer = BikeSerializer(bike)

        bike.delete()

        return JsonResponse(serializer.data, status = 200)

    raise NotFound()
