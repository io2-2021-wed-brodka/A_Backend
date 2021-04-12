from django.contrib import admin

from BikeRentalApi.models import Bike, BikeStation, Rental, AppUser, Admin, Tech

admin.site.register(Bike)
admin.site.register(BikeStation)
admin.site.register(Rental)
admin.site.register(Admin)
admin.site.register(AppUser)
admin.site.register(Tech)
