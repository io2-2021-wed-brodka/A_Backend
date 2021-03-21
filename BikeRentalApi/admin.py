from django.contrib import admin

from BikeRentalApi.models import Bike, BikeStation, Rental, User, Admin, Tech

admin.site.register(Bike)
admin.site.register(BikeStation)
admin.site.register(Rental)
admin.site.register(Admin)
admin.site.register(User)
admin.site.register(Tech)
