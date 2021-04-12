from rest_framework.exceptions import PermissionDenied, NotAuthenticated, AuthenticationFailed
from rest_framework.request import Request

from BikeRentalApi.enums import Role
from BikeRentalApi.models import Person, User, Admin, Tech, AppUser


def authenticate(request: Request):
    if 'Authorization' not in request.headers.keys():
        raise NotAuthenticated('No authorization header')

    auth_str_split = str(request.headers['Authorization']).split(' ')
    if len(auth_str_split) != 2:
        raise AuthenticationFailed('Incorrect authorization header')

    token = auth_str_split[1]
    try:
        person = User.objects.get(username = token).person
        if person.role == Role.Admin:
            return Admin.objects.get(id = person.id)
        elif person.role == Role.Tech:
            return Tech.objects.get(id = person.id)
        return AppUser.objects.get(id = person.id)
    except Person.DoesNotExist:
        raise PermissionDenied()
