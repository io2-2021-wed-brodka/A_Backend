from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request

from BikeRentalApi.enums import Role
from BikeRentalApi.models import Person, AppUser, Admin, Tech


# for now this uses basic auth, but may be changed to JWT in the future and become a little more complex then
def authenticate(request: Request):
    user = request.user
    try:
        person = Person.objects.get(user = user)
        if person.role == Role.Admin:
            return Admin.objects.get(user = user)
        elif person.role == Role.Tech:
            return Tech.objects.get(user = user)
        return AppUser.objects.get(user = user)
    except Person.DoesNotExist:
        raise PermissionDenied()
