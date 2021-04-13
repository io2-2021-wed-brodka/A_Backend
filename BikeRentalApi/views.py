import io

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import NotFound
from rest_framework import status

from BikeRentalApi.models import Bike, Rental, BikeStation
from BikeRentalApi.serializers.addBikeStationSerializer import AddBikeStationSerializer
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

        stream = io.BytesIO(request.body)
        serializer = AddBikeStationSerializer(data = JSONParser().parse(stream))

        if not serializer.is_valid():
            return JsonResponse({}, status = status.HTTP_400_BAD_REQUEST)

        station = serializer.create(serializer.validated_data)

        if station is None:
            return JsonResponse({}, status = status.HTTP_404_NOT_FOUND)

        bike = Bike()
        bike.bike_state = BikeState.Working
        bike.station = station
        bike.save()

        return JsonResponse(BikeSerializer(bike).data, safe = False, status = status.HTTP_201_CREATED)

    raise NotFound()


def bikes_detail(request, pk):
    user = authenticate(request)

    if request.method == 'DELETE':
        if user.role != Role.Admin:
            return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_401_UNAUTHORIZED)

        bike = get_object_or_404(Bike, pk = pk)
        data = BikeSerializer(bike).data

        bike.delete()

        return JsonResponse(data, safe = False, status = status.HTTP_200_OK)

    raise NotFound()


def stations_list(request):
    user = authenticate(request)

    if request.method == 'GET':
        bikes = BikeStation.objects.all()
        serializer = StationSerializer(bikes, many = True)
        return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)
    elif request.method == 'POST':
        if user.role != Role.Admin:
            return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_401_UNAUTHORIZED)

        stream = io.BytesIO(request.body)
        serializer = StationSerializer(data = JSONParser().parse(stream))

        if not serializer.is_valid():
            return JsonResponse({}, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return JsonResponse(serializer.data, safe = False, status = status.HTTP_201_CREATED)

    raise NotFound()


def station_detail(request, pk):
    user = authenticate(request)

    if request.method == 'GET':
        station = get_object_or_404(BikeStation, pk = pk)
        serializer = StationSerializer(station)

        return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if user.role != Role.Admin:
            return JsonResponse({"message": "Unauthorized"}, status = status.HTTP_401_UNAUTHORIZED)

        station = get_object_or_404(BikeStation, pk = pk)

        if Bike.objects.filter(station_id__exact = station.pk).count() > 0:
            return JsonResponse({'message': 'Station has bikes in it'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        data = StationSerializer(station).data
        station.delete()

        return JsonResponse(data, safe = False, status = status.HTTP_200_OK)

    raise NotFound()


def bikes_rented(request):
    user = authenticate(request)

    if request.method == 'GET':
        rentals = Rental.objects.filter(user_id__exact = user.pk)
        bikes = [rental.bike for rental in rentals]
        serializer = BikeSerializer(bikes, many = True)

        return JsonResponse(serializer.data, safe = False, status = status.HTTP_200_OK)
    elif request.method == 'POST':
        stream = io.BytesIO(request.body)
        serializer = RentBikeSerializer(data = JSONParser().parse(stream))

        if not serializer.is_valid():
            return JsonResponse({}, status = status.HTTP_400_BAD_REQUEST)

        bike = serializer.create(serializer.validated_data)

        if bike is None:
            return JsonResponse({'message': 'Bike not found'}, status = status.HTTP_404_NOT_FOUND)

        if bike.bike_state == BikeState.InService:
            return JsonResponse({'message': 'Bike is already rented'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        bike.bike_state = BikeState.InService
        bike.station = None

        rental = Rental()
        rental.bike = bike
        rental.user = user
        rental.start_date = timezone.now()
        rental.end_date = rental.start_date + timezone.timedelta(minutes = 30)

        rental.save()

        serializer = BikeSerializer(bike)
        return JsonResponse(serializer.data, safe = False, status = status.HTTP_201_CREATED)

    raise NotFound()
