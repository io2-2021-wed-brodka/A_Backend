from django_enumfield import enum


class BikeState(enum.Enum):
    Working = 0
    InService = 1
    Blocked = 2


class StationState(enum.Enum):
    Working = 0
    Blocked = 1
