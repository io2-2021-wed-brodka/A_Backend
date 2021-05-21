from django.contrib.auth.models import User

from BikeRentalApi.models import Admin


def run(*args):
    admin_user = User.objects.create_superuser(username = 'admin', password = 'admin', email = 'admin@bikes.com')
    Admin.objects.create(user = admin_user)
