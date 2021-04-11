from django.urls import path

from .views import bikes_list, bikes_detail, bikes_rented, stations_list, station_detail

urlpatterns = [
    path('bikes/', bikes_list, name = 'bikes_list'),
    path('bikes/<int:pk>', bikes_detail, name = 'bikes_detail'),
    path('bikes/rented/', bikes_rented, name = 'bikes_rented'),
    path('stations/', stations_list, name = 'station_list'),
    path('stations/<int:pk>', station_detail, name = 'station_detail')
]
