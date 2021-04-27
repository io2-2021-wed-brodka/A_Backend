from django.http import JsonResponse
from rest_framework import status

from BikeRentalApi.authentication import authenticate_bikes_user


class RoleRequired(object):
    def __init__(self, roles):
        self.roles = roles

    def __call__(self, f):
        def wrapped_f(*args):
            try:
                user = authenticate_bikes_user(args[0])
            except Exception:
                return JsonResponse(
                    {"message": "Unauthorized"},
                    status = status.HTTP_401_UNAUTHORIZED
                )

            return f(*args) if user.role in self.roles else JsonResponse(
                {"message": "Forbidden"},
                status = status.HTTP_403_FORBIDDEN
            )
        return wrapped_f
