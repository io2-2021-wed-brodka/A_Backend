from django.db import models
from django_enumfield import enum

from BikeRentalApi.enums import BikeState, StationState, MalfunctionState


class Person(models.Model):
    name = models.CharField(max_length = 100)
    lastname = models.CharField(max_length = 100)


class Admin(Person):
    pass


class Tech(Person):
    pass


class User(Person):
    pass


class BikeStation(models.Model):
    LocationName = models.CharField(max_length = 100)
    StationState = enum.EnumField(StationState, default = StationState.Working)


class Bike(models.Model):
    BikeState = enum.EnumField(BikeState, default = BikeState.Working)
    Station = models.ForeignKey(BikeStation, on_delete = models.CASCADE)


class Reservation(models.Model):
    ReservationDate = models.DateTimeField()
    ExpireDate = models.DateTimeField()
    User = models.ForeignKey(User, on_delete = models.CASCADE)
    Bike = models.ForeignKey(Bike, on_delete = models.CASCADE)


class Rental(models.Model):
    StartDate = models.DateTimeField()
    EndDate = models.DateTimeField()
    User = models.ForeignKey(User, on_delete = models.CASCADE)
    Bike = models.ForeignKey(Bike, on_delete = models.CASCADE)


class Malfunction(models.Model):
    DetectionDate = models.DateTimeField()
    Description = models.CharField(max_length = 200)
    State = enum.EnumField(MalfunctionState, default = MalfunctionState.NotFixed)
    Bike = models.ForeignKey(Bike, on_delete = models.CASCADE)
    ReportingUser = models.ForeignKey(User, on_delete = models.CASCADE)
