from rest_framework.request import Request

from BikeRentalApi.models import Person


# for now this uses basic auth, but may be changed to JWT in the future and become a little more complex then
def authenticate(request: Request) -> Person:
    user = request.user
    person = Person.objects.get(name = user.username)
    return person
