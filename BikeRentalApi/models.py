from django.db import models
from django_enumfield import enum

from BikeRentalApi.enums import BikeState, StationState, Role, UserState


class Person(models.Model):
    name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    role = enum.EnumField(Role, default = Role.User)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class Admin(Person):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = Role.Admin


class Tech(Person):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = Role.Tech


class User(Person):
    state = enum.EnumField(UserState, default = UserState.Active)


class BikeStation(models.Model):
    location_name = models.CharField(max_length = 100)
    state = enum.EnumField(StationState, default = StationState.Working)

    def __str__(self):
        return 'station ' + self.location_name


class Bike(models.Model):
    bike_state = enum.EnumField(BikeState, default = BikeState.Working)
    station = models.ForeignKey(BikeStation, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.bike_state} bike at {self.station} '


class Rental(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.user} rented {self.bike} from {self.start_date} to {self.end_date}'
