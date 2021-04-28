from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

from BikeRentalApi.models import AppUser


@api_view(['POST'])
def login(request):
    user = authenticate(request, username = request.data['login'], password = request.data['password'])
    if not user:
        return JsonResponse(
            {'message': 'Bad credentials'},
            status = status.HTTP_401_UNAUTHORIZED
        )

    return JsonResponse(
        {
            'token': user.username,
            'role': user.person.role.label
        },
        safe = False,
        status = status.HTTP_200_OK
    )


@api_view(['POST'])
def register(request):
    username = request.data['login']
    password = request.data['password']

    try:
        User.objects.get(username = username)
        return JsonResponse(
            {'message': 'Conflicting registration data'},
            status = status.HTTP_409_CONFLICT
        )
    except User.DoesNotExist:
        user = User.objects.create_user(username, f'{username}@bikes.com', password)
        AppUser.objects.create(user = user)
        return JsonResponse(
            {'token': username},
            status = status.HTTP_200_OK
        )


@api_view(['POST'])
def logout(request):
    return HttpResponse(status = status.HTTP_204_NO_CONTENT)
