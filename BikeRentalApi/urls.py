from django.urls import path

from BikeRentalApi import auth_views
from .views import bikes_list, bikes_detail, bikes_rented, stations_list, stations_detail, stations_detail_bikes


urlpatterns = [
    path('bikes/', bikes_list, name = 'bikes_list'),
    path('bikes/<int:pk>/', bikes_detail, name = 'bikes_detail'),
    path('bikes/rented/', bikes_rented, name = 'bikes_rented'),
    path('stations/', stations_list, name = 'station_list'),
    path('stations/<int:pk>/', stations_detail, name = 'station_detail'),
    path('stations/<int:pk>/bikes/', stations_detail_bikes, name = 'station_detail_bikes'),
    path('register/', auth_views.register, name = 'register'),
    path('login/', auth_views.login, name = 'login')
]
