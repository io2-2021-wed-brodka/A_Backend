from django.urls import path

from BikeRentalApi import auth_views
from .views import bikes_list, bikes_detail, bikes_rented, stations_list, stations_detail, stations_detail_bikes, \
    techs_list, techs_detail, stations_blocked, stations_blocked_detail, bikes_blocked, bikes_unblocked


urlpatterns = [
    path('bikes', bikes_list, name = 'bikes_list'),
    path('bikes/<int:pk>', bikes_detail, name = 'bikes_detail'),
    path('bikes/rented', bikes_rented, name = 'bikes_rented'),
    path('bikes/blocked', bikes_blocked, name = 'bikes_blocked'),
    path('bikes/blocked/<int:pk>', bikes_unblocked, name = 'bikes_unblocked'),
    path('stations', stations_list, name = 'station_list'),
    path('stations/<int:pk>', stations_detail, name = 'station_detail'),
    path('stations/<int:pk>/bikes', stations_detail_bikes, name = 'station_detail_bikes'),
    path('stations/blocked', stations_blocked, name = 'bikes_blocked'),
    path('stations/active', stations_blocked, name = 'bikes_blocked'),
    path('stations/blocked/<int:pk>', stations_blocked_detail, name = 'bikes_blocked_detail'),
    path('register', auth_views.register, name = 'register'),
    path('login', auth_views.login, name = 'login'),
    path('logout', auth_views.logout, name = 'logout'),
    path('techs', techs_list, name = 'techs_list'),
    path('techs/<int:pk>', techs_detail, name = 'techs_detail'),
]
