from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from BikeRentalApi.models import AppUser


@api_view(['POST'])
def login(request):
    print(request.headers)
    user = authenticate(request, username = request.data['login'], password = request.data['password'])
    print(user)
    if not user:
        return JsonResponse(status = 401, data = {'message': 'Bad credentials'})
    return JsonResponse({'token': user.username})


@api_view(['POST'])
def register(request):
    username = request.data['login']
    password = request.data['password']

    try:
        User.objects.get(username = username)
        return JsonResponse(status = 409, data = {'message': 'Conflicting registration data'})
    except User.DoesNotExist:
        user = User.objects.create_user(username, f'{username}@bikes.com', password)
        AppUser.objects.create(user = user)
        return JsonResponse({'token': username})
