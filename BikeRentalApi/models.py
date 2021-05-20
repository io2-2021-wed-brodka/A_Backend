from django.contrib.auth.models import User
from django.db import models
from django_enumfield import enum

from BikeRentalApi.enums import BikeState, StationState, Role, UserState, MalfunctionState


class Person(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    role = enum.EnumField(Role, default = Role.User)

    def __str__(self):
        return f'{self.user.username}'


class Admin(Person):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = Role.Admin


class Tech(Person):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = Role.Tech


class AppUser(Person):
    state = enum.EnumField(UserState, default = UserState.Active)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = Role.User


class BikeStation(models.Model):
    name = models.CharField(max_length = 100)
    state = enum.EnumField(StationState, default = StationState.Working)

    def __str__(self):
        return 'station ' + self.name


class Bike(models.Model):
    bike_state = enum.EnumField(BikeState, default = BikeState.Working)
    station = models.ForeignKey(BikeStation, on_delete = models.CASCADE, null = True, blank = True)

    def __str__(self):
        return f'{self.bike_state} bike at {self.station} '


class Rental(models.Model):
    start_date = models.DateTimeField()
    user = models.ForeignKey(Person, on_delete = models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.user} rented {self.bike} from {self.start_date}'


class Reservation(models.Model):
    start_date = models.DateTimeField()
    expire_date = models.DateTimeField()
    user = models.ForeignKey(Person, on_delete = models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.user} reserved {self.bike} from {self.start_date} to {self.expire_date}'


class Malfunction(models.Model):
    bike = models.ForeignKey(Bike, on_delete = models.CASCADE)
    description = models.CharField(max_length = 200)
    state = enum.EnumField(MalfunctionState, default = MalfunctionState.NotFixed)
    reporting_user = models.ForeignKey(User, on_delete = models.CASCADE)
