from django.urls import re_path

from BikeRentalApi import auth_views
from .views import bikes_list, bikes_detail, bikes_rented, stations_list, stations_detail, stations_detail_bikes, \
    techs_list, techs_detail, stations_blocked, stations_blocked_detail, bikes_blocked, bikes_unblocked, \
    stations_active, users_list, users_blocked_list, users_blocked_detail, malfunctions_list, stations_detail_bikes_all

urlpatterns = [
    re_path(r'^bikes/?$', bikes_list, name = 'bikes_list'),
    re_path(r'^bikes/(?P<pk>[0-9]+)/?$', bikes_detail, name = 'bikes_detail'),
    re_path(r'^bikes/rented/?$', bikes_rented, name = 'bikes_rented'),
    re_path(r'^bikes/blocked/?$', bikes_blocked, name = 'bikes_blocked'),
    re_path(r'^bikes/blocked/(?P<pk>[0-9]+)/?$', bikes_unblocked, name = 'bikes_unblocked'),
    re_path(r'^stations/?$', stations_list, name = 'station_list'),
    re_path(r'^stations/(?P<pk>[0-9]+)/?$', stations_detail, name = 'station_detail'),
    re_path(r'^stations/(?P<pk>[0-9]+)/bikes/?$', stations_detail_bikes, name = 'station_detail_bikes'),
    re_path(r'^stations/(?P<pk>[0-9]+)/bikes/all/?$', stations_detail_bikes_all, name = 'station_detail_bikes_all'),
    re_path(r'^stations/blocked/?$', stations_blocked, name = 'bikes_blocked'),
    re_path(r'^stations/active/?$', stations_active, name = 'bikes_blocked'),
    re_path(r'^stations/blocked/(?P<pk>[0-9]+)/?$', stations_blocked_detail, name = 'bikes_blocked_detail'),
    re_path(r'^register/?$', auth_views.register, name = 'register'),
    re_path(r'^login/?$', auth_views.login, name = 'login'),
    re_path(r'^logout/?$', auth_views.logout, name = 'logout'),
    re_path(r'^techs/?$', techs_list, name = 'techs_list'),
    re_path(r'^techs/(?P<pk>[0-9]+)/?$', techs_detail, name = 'techs_detail'),
    re_path(r'^users/?$', users_list, name = 'users_list'),
    re_path(r'^users/blocked/?$', users_blocked_list, name = 'users_blocked_list'),
    re_path(r'^users/blocked/(?P<pk>[0-9]+)/?$', users_blocked_detail, name = 'users_blocked_detail'),
    re_path(r'^malfunctions/?$', malfunctions_list, name = 'malfunctions_list'),

]
