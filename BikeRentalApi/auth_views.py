from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from BikeRentalApi.models import AppUser


@api_view(['POST'])
def login(request):
    return JsonResponse({'token': request.data['login']})


@api_view(['POST'])
def register(request):
    username = request.data['login']
    password = request.data['password']
    user = User.objects.create(username = username, password = password, email = f'{username}@bikes.com')
    AppUser.objects.create(user = user)
    return JsonResponse({'token': username})
