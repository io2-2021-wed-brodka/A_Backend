from django_enumfield import enum


class BikeState(enum.Enum):
    Working = 0
    InService = 1
    Blocked = 2


class StationState(enum.Enum):
    Working = 0
    Blocked = 1


class UserState(enum.Enum):
    Active = 0
    Banned = 1


class Role(enum.Enum):
    User = 0
    Tech = 1
    Admin = 2
