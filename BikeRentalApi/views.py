from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import PermissionDenied, NotFound

from BikeRentalApi.models import Bike, Rental, BikeStation
from BikeRentalApi.serializers.bikeSerializer import BikeSerializer
from BikeRentalApi.serializers.stationSerializer import StationSerializer
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


def stations_list(request):
    user = authenticate(request)

    if request.method == 'GET':
        bikes = BikeStation.objects.all()
        serializer = StationSerializer(bikes, many = True)
        return JsonResponse(serializer.data, safe = False, status = 200)
    elif request.method == 'POST':
        if user.role != Role.Admin:
            raise PermissionDenied()

        data = JSONParser().parse(request)
        serializer = StationSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)

    raise NotFound()


def station_detail(request, pk):
    user = authenticate(request)

    if request.method == 'GET':
        station = get_object_or_404(BikeStation, pk = pk)
        serializer = StationSerializer(station)

        return JsonResponse(serializer.data, status = 200)
    elif request.method == 'DELETE':
        if user.role != Role.Admin:
            raise PermissionDenied()

        station = get_object_or_404(BikeStation, pk = pk)
        serializer = StationSerializer(station)
        station.delete()

        return JsonResponse(serializer.data, status = 200)

    raise NotFound()
