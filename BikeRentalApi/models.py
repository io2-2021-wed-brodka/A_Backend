from django.db import models
from django_enumfield import enum

from BikeRentalApi.enums import BikeState, StationState


class Person(models.Model):
    name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)


class Admin(Person):
    pass


class Tech(Person):
    pass


class User(Person):
    pass


class BikeStation(models.Model):
    location_name = models.CharField(max_length = 100)
    state = enum.EnumField(StationState, default = StationState.Working)


class Bike(models.Model):
    bike_state = enum.EnumField(BikeState, default = BikeState.Working)
    station = models.ForeignKey(BikeStation, on_delete = models.CASCADE)


class Rental(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete = models.CASCADE)
