from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework import status

from BikeRentalApi.models import Bike, Rental, BikeStation
from BikeRentalApi.serializers.bikeSerializer import BikeSerializer
from BikeRentalApi.serializers.stationSerializer import StationSerializer
from BikeRentalApi.serializers.rentBikeSerializer import RentBikeSerializer
from BikeRentalApi.authentication import authenticate
from BikeRentalApi.enums import Role, BikeState


def bikes_list(request):
    user = authenticate(request)

    if request.method == 'GET':
        if user.role < Role.Tech:
            return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_401_UNAUTHORIZED)

        bikes = Bike.objects.all()
        serializer = BikeSerializer(bikes, many = True)
        return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)
    elif request.method == 'POST':
        if user.role != Role.Admin:
            return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_401_UNAUTHORIZED)

        serializer = BikeSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe = False, status = status.HTTP_201_CREATED)

    return JsonResponse({}, status = status.HTTP_404_NOT_FOUND)


def bikes_detail(request, pk):
    user = authenticate(request)

    if request.method == 'DELETE':
        if user.Role != Role.Admin:
            return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_401_UNAUTHORIZED)

        bike = get_object_or_404(Bike, pk = pk)
        serializer = BikeSerializer(bike)
        bike.delete()

        return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)

    return JsonResponse({}, status = status.HTTP_404_NOT_FOUND)


def stations_list(request):
    user = authenticate(request)

    if request.method == 'GET':
        bikes = BikeStation.objects.all()
        serializer = StationSerializer(bikes, many = True)
        return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)
    elif request.method == 'POST':
        if user.role != Role.Admin:
            raise PermissionDenied()

        data = JSONParser().parse(request)
        serializer = StationSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe = False, status = status.HTTP_201_CREATED)

    return JsonResponse({}, status = status.HTTP_404_NOT_FOUND)


def station_detail(request, pk):
    user = authenticate(request)

    if request.method == 'GET':
        station = get_object_or_404(BikeStation, pk = pk)
        serializer = StationSerializer(station)

        return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if user.role != Role.Admin:
            raise PermissionDenied()

        station = get_object_or_404(BikeStation, pk = pk)
        serializer = StationSerializer(station)
        station.delete()

        return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)

    return JsonResponse({}, status = status.HTTP_404_NOT_FOUND)


def bikes_rented(request):
    user = authenticate(request)

    if request.method == 'GET':
        rentals = Rental.objects.filter(user_id__exact = user.pk)
        bikes = [rental.bike for rental in rentals]
        serializer = BikeSerializer(bikes, many = True)

        return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = RentBikeSerializer(data = request.data)

        if not serializer.is_valid():
            raise NotFound()

        bike = serializer.create(serializer.validated_data)
        bike.bike_state = BikeState.InService
        bike.station = None

        rental = Rental()
        rental.bike = bike
        rental.user = user
        rental.start_date = timezone.now()
        rental.end_date = rental.start_date + timezone.timedelta(minutes = 30)

        bike.save()
        rental.save()

        serializer = BikeSerializer(bike)
        return JsonResponse(serializer.data, safe = False, status = status.HTTP_201_CREATED)

    return JsonResponse({}, status = status.HTTP_404_NOT_FOUND)
