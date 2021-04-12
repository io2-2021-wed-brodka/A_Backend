from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from BikeRentalApi.models import AppUser


@api_view(['POST'])
def login(request):
    try:
        user = User.objects.get(username = request.data['login'], password = request.data['password'])
        return JsonResponse({'token': user.username})
    except User.DoesNotExist:
        return JsonResponse(status = 401, data = {'message': 'Bad credentials'})


@api_view(['POST'])
def register(request):
    username = request.data['login']
    password = request.data['password']

    user, new = User.objects.get_or_create(username = username)
    if not new:
        return JsonResponse(status = 409, data = {'message': 'Conflicting registration data'})

    user.password = password
    user.email = f'{username}@bikes.com'
    user.save()

    AppUser.objects.create(user = user)
    return JsonResponse({'token': username})
