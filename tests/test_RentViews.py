from datetime import date, time, datetime

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, Rental, BikeStation
from BikeRentalApi.views import bikes_list


@pytest.mark.django_db
class TestRentViews:

    @pytest.fixture
    def tech(self):
        tech = User.objects.create(
            username = 'Mariusz', first_name = 'Mariusz', last_name = 'Tester', email = 'mariusz@test.com',
            password = 'test123')
        return models.Tech.objects.create(user = tech)

    @pytest.fixture
    def user(self):
        user = User.objects.create(
            username = 'Janek', first_name = 'Janek', last_name = 'Tester', email = 'Janek@test.com',
            password = 'test1234')
        return models.AppUser.objects.create(user = user)

    @pytest.fixture
    def station(self):
        return BikeStation.objects.create(name = 'Test station', state = StationState.Working)

    @pytest.fixture
    def bike(self, user, station):
        bike = Bike.objects.create(station = station, bike_state = BikeState.Working)
        rental_date = date(2005, 7, 14)
        rental_start_time = time(12, 30)
        rental_end_time = time(12, 55)
        rental_start_datetime = datetime.combine(rental_date, rental_start_time, tzinfo = timezone.utc)
        rental_end_datetime = datetime.combine(rental_date, rental_end_time, tzinfo = timezone.utc)
        Rental.objects.create(user = user, bike = bike, start_date = rental_start_datetime,
                              end_date = rental_end_datetime)
        return bike

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_get_bikes_user_status(self, factory, user):
        request = factory.get('/api/bikes')
        request.user = user.user

        response = bikes_list(request)
        assert response.status_code == 401

    def test_get_bikes_tech_status(self, factory, tech):
        request = factory.get('/api/bikes')
        request.user = tech.user

        response = bikes_list(request)
        assert response.status_code == 200

    def test_get_bikes_tech_body(self, factory, user, station, bike, tech):
        request = factory.get('api/bikes')
        request.user = tech.user

        response = bikes_list(request)

        assert json.loads(response.content) == [
            {
                'id': 1,
                'station': {
                    'id': 1,
                    'name': 'Test station'
                },
                'bike_state': 0,
                'user': {
                    'id': 3,
                    'name': 'Janek'
                }
            }
        ]
