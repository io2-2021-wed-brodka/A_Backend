from django.utils.translation import gettext_lazy
from django_enumfield import enum


class BikeState(enum.Enum):
    Working = 0
    InService = 1
    Blocked = 2
    Reserved = 3

    __labels__ = {
        Working: gettext_lazy("available"),
        InService: gettext_lazy("rented"),
        Blocked: gettext_lazy("blocked"),
        Reserved: gettext_lazy("reserved")
    }


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
