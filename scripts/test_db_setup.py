import json

from django.contrib.auth.models import User

from BikeRentalApi.models import BikeStation, Bike, Admin


def insert_bike(json_obj):
    Bike.objects.create(id = json_obj['id'], station_id = json_obj['station'], bike_state = json_obj['status'])


def insert_station(json_obj):
    BikeStation.objects.create(id = json_obj['id'], name = json_obj['name'], state = json_obj['status'])


def setup_table(filename: str, model, insert_record):
    # first clear table
    for record in model.objects.all():
        record.delete()

    # create all objects from JSON array
    with open(filename) as file:
        json_list = json.load(file)
        for json_obj in json_list:
            insert_record(json_obj)


def run(*args):
    if len(args) != 2:
        print('Specify JSON files containg stations and bikes')
        exit(1)

    setup_table(args[0], BikeStation, insert_station)
    setup_table(args[1], Bike, insert_bike)

    admin_user = User.objects.create_superuser(username = 'admin', password = 'admin', email = 'admin@bikes.com')
    Admin.objects.create(user = admin_user)
