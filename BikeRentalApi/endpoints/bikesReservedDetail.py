from django.http import JsonResponse, HttpResponse
from rest_framework import status

from BikeRentalApi.authentication import authenticate_bikes_user
from BikeRentalApi.decorators.roleRequired import RoleRequired
from BikeRentalApi.enums import Role, BikeState, UserState
from BikeRentalApi.models import Reservation, AppUser

# DELETE: cancel a reservation


@RoleRequired([Role.User, Role.Tech, Role.Admin])
def delete(request, pk):
    user = authenticate_bikes_user(request)
    if isinstance(user, AppUser) and user.state == UserState.Banned:
        return JsonResponse({'message': 'User is banned'}, status = status.HTTP_403_FORBIDDEN)

    try:
        reservation = Reservation.objects.get(bike_id = pk)
    except Reservation.DoesNotExist:
        return JsonResponse(
            {'message': "Reservation not found"},
            status = status.HTTP_404_NOT_FOUND
        )

    if reservation.user.pk != user.pk:
        return JsonResponse(
            {'message': "Reservation was not made by calling user"},
            status = status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    bike = reservation.bike
    bike.bike_state = BikeState.Working
    bike.save()

    reservation.delete()

    return HttpResponse(status = status.HTTP_204_NO_CONTENT)
