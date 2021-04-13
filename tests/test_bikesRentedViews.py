from datetime import date, time, datetime

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, Rental, BikeStation
from BikeRentalApi.views import bikes_rented


@pytest.mark.django_db
class TestBikesRentedViews:

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
    def admin(self):
        user = User.objects.create(
            username = 'Pawel', first_name = 'Pawel', last_name = 'Tester', email = 'Pawel@test.com',
            password = 'test1234')
        return models.Admin.objects.create(user = user)

    @pytest.fixture
    def station(self):
        return BikeStation.objects.create(name = 'Test station', state = StationState.Working)

    @pytest.fixture
    def bike1(self, user, station):
        bike = Bike.objects.create(station = None, bike_state = BikeState.InService)
        rental_date = date(2005, 7, 14)
        rental_start_time = time(12, 30)
        rental_end_time = time(12, 55)
        rental_start_datetime = datetime.combine(rental_date, rental_start_time, tzinfo = timezone.utc)
        rental_end_datetime = datetime.combine(rental_date, rental_end_time, tzinfo = timezone.utc)
        Rental.objects.create(user = user, bike = bike, start_date = rental_start_datetime,
                              end_date = rental_end_datetime)
        return bike

    @pytest.fixture
    def bike2(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Working)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_get_bikes_rented_status_user(self, user, factory):
        request = factory.get('/api/bikes/rented')
        request.user = user.user

        response = bikes_rented(request)
        assert response.status_code == 200

    def test_get_bikes_rented_status_tech(self, tech, factory):
        request = factory.get('/api/bikes/rented')
        request.user = tech.user

        response = bikes_rented(request)
        assert response.status_code == 200

    def test_get_bikes_rented_status_admin(self, admin, factory):
        request = factory.get('/api/bikes/rented')
        request.user = admin.user

        response = bikes_rented(request)
        assert response.status_code == 200

    def test_get_bikes_rented_response(self, user, factory, bike1, station):
        request = factory.get('/api/bikes/rented')
        request.user = user.user

        response = bikes_rented(request)
        assert json.loads(response.content) == [
            {
                'id': bike1.pk,
                'station': None,
                'bike_state': BikeState.InService,
                'user': {
                    'id': user.pk,
                    'name': user.user.first_name
                }
            }
        ]

    def test_post_bikes_rented_user_status(self, user, bike2, factory):
        body = json.dumps({"id": bike2.pk})
        request = factory.post('api/bikes/rented', content_type = 'application/json', data = body)
        request.user = user.user

        response = bikes_rented(request)
        assert response.status_code == 201

    def test_post_bikes_rented_bad_request(self, user, factory):
        body = json.dumps({"id": 1337})
        request = factory.post('api/bikes/rented', content_type = 'application/json', data = body)
        request.user = user.user

        response = bikes_rented(request)
        assert response.status_code == 404

    def test_post_bikes_rented_response(self, user, station, bike2, factory):
        body = json.dumps({"id": bike2.pk})
        request = factory.post('api/bikes/rented', content_type = 'application/json', data = body)
        request.user = user.user

        response = bikes_rented(request)
        assert json.loads(response.content) == {
            'id': bike2.pk,
            'station': None,
            'bike_state': BikeState.InService,
            'user': {
                'id': user.pk,
                'name': user.user.first_name
            }
        }
