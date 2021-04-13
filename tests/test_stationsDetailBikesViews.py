import pytest
from datetime import date, time, datetime
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, BikeStation, Rental
from BikeRentalApi.views import stations_detail_bikes


@pytest.mark.django_db
class TestStationsDetailViews:

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
    def user2(self):
        user = User.objects.create(
            username = 'Bartosz', first_name = 'Bartosz', last_name = 'Tester', email = 'Bartosz@test.com',
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
    def empty_station(self):
        return BikeStation.objects.create(name = 'Empty station', state = StationState.Working)

    @pytest.fixture
    def bike(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Working)

    @pytest.fixture
    def bike_rented(self, user, station):
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
    def factory(self):
        return APIRequestFactory()

    def test_get_stations_detail_bikes_user_status(self, factory, station, user):
        request = factory.get(f'/api/stations/{station.pk}/bikes')
        request.user = user.user

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == 200

    def test_get_stations_detail_bikes_tech_status(self, factory, station, tech):
        request = factory.get(f'/api/stations/{station.pk}/bikes')
        request.user = tech.user

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == 200

    def test_get_stations_detail_bikes_admin_status(self, factory, station, admin):
        request = factory.get(f'/api/stations/{station.pk}/bikes')
        request.user = admin.user

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == 200

    def test_get_stations_detail_bikes_user_response(self, factory, station, bike, user):
        request = factory.get(f'/api/stations/{station.pk}/bikes')
        request.user = user.user

        response = stations_detail_bikes(request, station.pk)
        assert json.loads(response.content) == [
            {
                'id': bike.pk,
                'user': None,
                'bike_state': BikeState.Working,
                'station': {
                    'id': station.pk,
                    'name': station.name
                }
            }
        ]

    def test_post_stations_detail_bikes_user_status(self, factory, bike_rented, station, user):
        body = json.dumps({'id': bike_rented.pk})
        request = factory.post(f'/api/stations/{station.pk}/bikes', content_type = 'application/json', data = body)
        request.user = user.user

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == 201

    def test_post_stations_detail_bikes_user_response(self, factory, bike_rented, station, user):
        body = json.dumps({'id': bike_rented.pk})
        request = factory.post(f'/api/stations/{station.pk}/bikes', content_type = 'application/json', data = body)
        request.user = user.user

        response = stations_detail_bikes(request, station.pk)
        assert json.loads(response.content) == {
            'id': bike_rented.pk,
            'bike_state': BikeState.Working,
            'user': None,
            'station': {
                'id': station.pk,
                'name': station.name
            }
        }

    def test_post_stations_detail_bikes_bad_request_bike(self, factory, station, user):
        body = json.dumps({'id': 13313131})
        request = factory.post(f'/api/stations/{station.pk}/bikes', content_type = 'application/json', data = body)
        request.user = user.user

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == 404

    def test_post_stations_detail_bikes_bad_request_station(self, factory, bike_rented, user):
        body = json.dumps({'id': bike_rented.pk})
        request = factory.post(f'/api/stations/{1234}/bikes', content_type = 'application/json', data = body)
        request.user = user.user

        response = stations_detail_bikes(request, 1234)
        assert response.status_code == 404

    def test_post_stations_detail_bikes_not_own_rental(self, factory, bike_rented, station, user, user2):
        body = json.dumps({'id': bike_rented.pk})
        request = factory.post(f'/api/stations/{station.pk}/bikes', content_type = 'application/json', data = body)
        request.user = user2.user

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == 422

    def test_post_stations_detail_bikes_not_rented(self, factory, bike, station, user):
        body = json.dumps({'id': bike.pk})
        request = factory.post(f'/api/stations/{station.pk}/bikes', content_type = 'application/json', data = body)
        request.user = user.user

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == 422