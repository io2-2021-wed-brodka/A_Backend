from django.urls import path

from BikeRentalApi import auth_views

urlpatterns = [
    path('register', auth_views.register, name = 'register')
]
