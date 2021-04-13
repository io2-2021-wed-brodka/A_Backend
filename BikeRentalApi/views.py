from rest_framework.exceptions import NotFound

from .authentication import authenticate
from .endpoints import bikesList, bikesDetail, stationsList, stationsDetail, bikesRented, stationsDetailBikes


def bikes_list(request):
    user = authenticate(request)

    if request.method == 'GET':
        return bikesList.get(user)
    elif request.method == 'POST':
        return bikesList.post(request, user)

    raise NotFound()


def bikes_detail(request, pk):
    user = authenticate(request)

    if request.method == 'DELETE':
        return bikesDetail.delete(user, pk)

    raise NotFound()


def bikes_rented(request):
    user = authenticate(request)

    if request.method == 'GET':
        return bikesRented.get(user)
    elif request.method == 'POST':
        return bikesRented.post(request, user)

    raise NotFound()


def stations_list(request):
    user = authenticate(request)

    if request.method == 'GET':
        return stationsList.get()
    elif request.method == 'POST':
        return stationsList.post(request, user)

    raise NotFound()


def stations_detail(request, pk):
    user = authenticate(request)

    if request.method == 'GET':
        return stationsDetail.get(pk)
    elif request.method == 'DELETE':
        return stationsDetail.delete(user, pk)

    raise NotFound()


def stations_detail_bikes(request, pk):
    user = authenticate(request)

    if request.method == 'GET':
        return stationsDetailBikes.get(pk)
    elif request.method == 'POST':
        return stationsDetailBikes.post(request, user, pk)

    raise NotFound()
