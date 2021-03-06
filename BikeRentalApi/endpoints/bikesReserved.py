import io
from datetime import timedelta

from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework.parsers import JSONParser
from rest_framework import status

from A_Backend.common_settings import TIME_DELTA, BIKE_RESERVATION_LIMIT
from BikeRentalApi.authentication import authenticate_bikes_user
from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.models import AppUser, Reservation
from BikeRentalApi.serializers.rentBikeSerializer import RentBikeSerializer
from BikeRentalApi.enums import BikeState, Role, UserState, StationState

from BikeRentalApi.serializers.reservationSerializer import ReservationSerializer

# GET: list all reservations made by a given user
# POST: make a reservation for a bike


@RoleRequired([Role.User, Role.Tech, Role.Admin])
def get(request):
    user = authenticate_bikes_user(request)

    reservations = Reservation.objects.filter(user_id__exact = user.pk)
    serializer = ReservationSerializer(reservations, many = True)

    return JsonResponse(
        {"bikes": serializer.data},
        safe = False,
        status = status.HTTP_200_OK
    )


@RoleRequired([Role.User, Role.Tech, Role.Admin])
def post(request):
    user = authenticate_bikes_user(request)
    if isinstance(user, AppUser) and user.state == UserState.Banned:
        return JsonResponse(
            {'message': 'User is banned'},
            status = status.HTTP_403_FORBIDDEN
        )

    if Reservation.objects.filter(user_id = user.pk).count() >= BIKE_RESERVATION_LIMIT:
        return JsonResponse(
            {'message': 'Limit of reservations reached'},
            status = status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    stream = io.BytesIO(request.body)
    serializer = RentBikeSerializer(data = JSONParser().parse(stream))

    if not serializer.is_valid():
        return HttpResponse(status = status.HTTP_400_BAD_REQUEST)

    bike = serializer.create(serializer.validated_data)

    if bike is None:
        return JsonResponse(
            {'message': 'Bike not found'},
            status = status.HTTP_404_NOT_FOUND
        )

    if bike.bike_state in [BikeState.InService, BikeState.Blocked, BikeState.Reserved]:
        return JsonResponse(
            {'message': 'Bike is already reserved, rented or blocked'},
            status = status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    if bike.station.state == StationState.Blocked:
        return JsonResponse(
            {'message': 'Station is blocked'},
            status = status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    bike.bike_state = BikeState.Reserved
    bike.save()

    # approximate start_time to the next full minute
    start_date = timezone.now()
    approx_start_date = start_date + timedelta(seconds = 59, milliseconds = 999)
    approx_start_date -= timedelta(seconds = approx_start_date.second, microseconds = approx_start_date.microsecond)

    reservation = Reservation.objects.create(
        bike = bike,
        user = user,
        start_date = start_date,
        expire_date = approx_start_date + TIME_DELTA
    )
    reservation.save()

    serializer = ReservationSerializer(reservation)

    return JsonResponse(
        serializer.data,
        safe = False,
        status = status.HTTP_201_CREATED
    )
