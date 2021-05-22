from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import NotFound

from .endpoints import bikesList, bikesDetail, stationsList, stationsDetail, bikesRented, stationsDetailBikes, \
    techsList, techsDetail, stationsBlocked, stationsDetailsBlocked, bikesBlocked, bikesUnblocked, stationsActive, \
    usersList, usersBlockedList, usersBlockedDetail, malfunctionsList, malfunctionsDetail, bikesReserved, \
    bikesReservedDetail


@csrf_exempt
def bikes_list(request):
    if request.method == 'GET':
        return bikesList.get(request)
    elif request.method == 'POST':
        return bikesList.post(request)

    raise NotFound()


@csrf_exempt
def malfunctions_list(request):
    if request.method == 'GET':
        return malfunctionsList.get(request)
    elif request.method == 'POST':
        return malfunctionsList.post(request)

    raise NotFound()


@csrf_exempt
def malfunctions_detail(request, pk):
    if request.method == 'DELETE':
        return malfunctionsDetail.delete(request, pk)

    raise NotFound()


@csrf_exempt
def bikes_detail(request, pk):
    if request.method == 'DELETE':
        return bikesDetail.delete(request, pk)

    raise NotFound()


@csrf_exempt
def bikes_blocked(request):
    if request.method == 'GET':
        return bikesBlocked.get(request)
    elif request.method == 'POST':
        return bikesBlocked.post(request)

    raise NotFound()


@csrf_exempt
def bikes_unblocked(request, pk):
    if request.method == 'DELETE':
        return bikesUnblocked.delete(request, pk)

    raise NotFound()


@csrf_exempt
def bikes_reserved(request):
    if request.method == 'GET':
        return bikesReserved.get(request)
    elif request.method == 'POST':
        return bikesReserved.post(request)

    raise NotFound()


@csrf_exempt
def bikes_reserved_detail(request, pk):
    if request.method == 'DELETE':
        return bikesReservedDetail.delete(request, pk)

    raise NotFound()


@csrf_exempt
def bikes_rented(request):
    if request.method == 'GET':
        return bikesRented.get(request)
    elif request.method == 'POST':
        return bikesRented.post(request)

    raise NotFound()


@csrf_exempt
def stations_list(request):
    if request.method == 'GET':
        return stationsList.get(request)
    elif request.method == 'POST':
        return stationsList.post(request)

    raise NotFound()


@csrf_exempt
def stations_detail(request, pk):
    if request.method == 'GET':
        return stationsDetail.get(request, pk)
    elif request.method == 'DELETE':
        return stationsDetail.delete(request, pk)

    raise NotFound()


@csrf_exempt
def stations_detail_bikes(request, pk):
    if request.method == 'GET':
        return stationsDetailBikes.get(request, pk)
    elif request.method == 'POST':
        return stationsDetailBikes.post(request, pk)

    raise NotFound()


@csrf_exempt
def stations_detail_bikes_all(request, pk):
    if request.method == 'GET':
        return stationsDetailBikes.get_all(request, pk)
    raise NotFound()


@csrf_exempt
def stations_blocked(request):
    if request.method == 'GET':
        return stationsBlocked.get(request)
    elif request.method == 'POST':
        return stationsBlocked.post(request)

    raise NotFound()


@csrf_exempt
def stations_active(request):
    if request.method == 'GET':
        return stationsActive.get(request)

    raise NotFound()


@csrf_exempt
def stations_blocked_detail(request, pk):
    if request.method == 'DELETE':
        return stationsDetailsBlocked.delete(request, pk)

    raise NotFound()


@csrf_exempt
def techs_list(request):
    if request.method == 'POST':
        return techsList.post(request)
    elif request.method == 'GET':
        return techsList.get(request)

    raise NotFound()


@csrf_exempt
def techs_detail(request, pk):
    if request.method == 'DELETE':
        return techsDetail.delete(request, pk)
    elif request.method == 'GET':
        return techsDetail.get(request, pk)

    raise NotFound()


def users_list(request):
    if request.method == 'GET':
        return usersList.get(request)

    raise NotFound()


@csrf_exempt
def users_blocked_list(request):
    if request.method == 'GET':
        return usersBlockedList.get(request)
    elif request.method == 'POST':
        return usersBlockedList.post(request)

    raise NotFound()


@csrf_exempt
def users_blocked_detail(request, pk):
    if request.method == 'DELETE':
        return usersBlockedDetail.delete(request, pk)

    raise NotFound()
