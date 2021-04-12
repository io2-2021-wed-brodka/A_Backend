from django.urls import path

from BikeRentalApi import auth_views

urlpatterns = [
    path('register', auth_views.register, name = 'register'),
    path('login', auth_views.login, name = 'login')
]
