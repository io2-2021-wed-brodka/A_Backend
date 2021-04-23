from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import NotFound

from .authentication import authenticate_bikes_user
from .endpoints import bikesList, bikesDetail, stationsList, stationsDetail, bikesRented, stationsDetailBikes, \
    techsList, techsDetail, stationsBlocked, stationsDetailsBlocked, bikesBlocked, bikesUnblocked



@csrf_exempt
def bikes_list(request):
    user = authenticate_bikes_user(request)

    if request.method == 'GET':
        return bikesList.get(user)
    elif request.method == 'POST':
        return bikesList.post(request, user)

    raise NotFound()


@csrf_exempt
def bikes_detail(request, pk):
    user = authenticate_bikes_user(request)
    if request.method == 'DELETE':
        return bikesDetail.delete(user, pk)

    raise NotFound()


@csrf_exempt
def bikes_blocked(request):
    user = authenticate_bikes_user(request)

    if request.method == 'GET':
        return bikesBlocked.get(user)
    elif request.method == 'POST':
        return bikesBlocked.post(request, user)

    raise NotFound()


@csrf_exempt
def bikes_unblocked(request, pk):
    user = authenticate_bikes_user(request)
    if request.method == 'DELETE':
        return bikesUnblocked.delete(user, pk)

    raise NotFound()


@csrf_exempt
def bikes_rented(request):
    user = authenticate_bikes_user(request)

    if request.method == 'GET':
        return bikesRented.get(user)
    elif request.method == 'POST':
        return bikesRented.post(request, user)

    raise NotFound()


def stations_list(request):
    user = authenticate_bikes_user(request)

    if request.method == 'GET':
        return stationsList.get()
    elif request.method == 'POST':
        return stationsList.post(request, user)

    raise NotFound()


@csrf_exempt
def stations_detail(request, pk):
    user = authenticate_bikes_user(request)

    if request.method == 'GET':
        return stationsDetail.get(pk)
    elif request.method == 'DELETE':
        return stationsDetail.delete(user, pk)

    raise NotFound()


@csrf_exempt
def stations_detail_bikes(request, pk):
    user = authenticate_bikes_user(request)

    if request.method == 'GET':
        return stationsDetailBikes.get(pk)
    elif request.method == 'POST':
        return stationsDetailBikes.post(request, user, pk)

    raise NotFound()


@csrf_exempt
def stations_blocked(request):
    user = authenticate_bikes_user(request)

    if request.method == 'GET':
        return stationsBlocked.get(user)
    elif request.method == 'POST':
        return stationsBlocked.post(request, user)

    raise NotFound()


@csrf_exempt
def stations_blocked_detail(request, pk):
    user = authenticate_bikes_user(request)

    if request.method == 'DELETE':
        return stationsDetailsBlocked.delete(user, pk)

    raise NotFound()


@csrf_exempt
def techs_list(request):
    user = authenticate_bikes_user(request)

    if request.method == 'POST':
        return techsList.post(request, user)
    elif request.method == 'GET':
        return techsList.get(user)

    raise NotFound()


@csrf_exempt
def techs_detail(request, pk):
    user = authenticate_bikes_user(request)

    if request.method == 'DELETE':
        return techsDetail.delete(user, pk)
    elif request.method == 'GET':
        return techsDetail.get(user, pk)

    raise NotFound()
