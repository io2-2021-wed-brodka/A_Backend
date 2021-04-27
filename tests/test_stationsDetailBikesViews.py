import pytest
from datetime import date, time, datetime
from django.contrib.auth.models import User
from rest_framework import status
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
    def blocked_station(self):
        return BikeStation.objects.create(name = 'Blocked station', state = StationState.Blocked)

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
        rental_start_datetime = datetime.combine(rental_date, rental_start_time, tzinfo = timezone.utc)
        Rental.objects.create(user = user, bike = bike, start_date = rental_start_datetime)
        return bike

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_get_stations_detail_bikes_user_status(self, factory, station, user):
        request = factory.get(f'/api/stations/{station.pk}/bikes')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == status.HTTP_200_OK

    def test_get_stations_detail_bikes_tech_status(self, factory, station, tech):
        request = factory.get(f'/api/stations/{station.pk}/bikes')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == status.HTTP_200_OK

    def test_get_stations_detail_bikes_admin_status(self, factory, station, admin):
        request = factory.get(f'/api/stations/{station.pk}/bikes')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == status.HTTP_200_OK

    def test_get_stations_detail_bikes_user_response(self, factory, station, bike, user):
        request = factory.get(f'/api/stations/{station.pk}/bikes')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = stations_detail_bikes(request, station.pk)
        assert json.loads(response.content) == {
            "bikes": [
                {
                    'id': str(bike.pk),
                    'user': None,
                    'status': BikeState.Working.label,
                    'station': {
                        'id': str(station.pk),
                        'name': station.name,
                        'status': station.state.label,
                        'activeBikesCount': Bike.objects.filter(station__pk = station.pk,
                                                                bike_state = BikeState.Working).count()
                    }
                }
            ]
        }

    def test_post_stations_detail_bikes_user_status(self, factory, bike_rented, station, user):
        body = json.dumps({'id': str(bike_rented.pk)})
        request = factory.post(f'/api/stations/{station.pk}/bikes', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_stations_detail_bikes_user_response(self, factory, bike_rented, station, user):
        body = json.dumps({'id': str(bike_rented.pk)})
        request = factory.post(f'/api/stations/{station.pk}/bikes', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = stations_detail_bikes(request, station.pk)
        assert json.loads(response.content) == {
            'id': str(bike_rented.pk),
            'status': BikeState.Working.label,
            'user': None,
            'station': {
                'id': str(station.pk),
                'name': station.name,
                'status': station.state.label,
                'activeBikesCount': Bike.objects.filter(station__pk = station.pk,
                                                        bike_state = BikeState.Working).count()
            }
        }

    def test_post_stations_detail_bikes_bad_request_bike(self, factory, station, user):
        body = json.dumps({'id': '13313131'})
        request = factory.post(f'/api/stations/{station.pk}/bikes', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_stations_detail_bikes_bad_request_station(self, factory, bike_rented, user):
        body = json.dumps({'id': str(bike_rented.pk)})
        request = factory.post(f'/api/stations/{1234}/bikes', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = stations_detail_bikes(request, 1234)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_stations_detail_bikes_not_own_rental(self, factory, bike_rented, station, user, user2):
        body = json.dumps({'id': str(bike_rented.pk)})
        request = factory.post(f'/api/stations/{station.pk}/bikes', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user2.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_post_stations_detail_bikes_not_rented(self, factory, bike, station, user):
        body = json.dumps({'id': str(bike.pk)})
        request = factory.post(f'/api/stations/{station.pk}/bikes', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = stations_detail_bikes(request, station.pk)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_blocked_stations_detail_bikes_user_status(self, factory, blocked_station, user):
        request = factory.get(f'/api/stations/{blocked_station.pk}/bikes')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = stations_detail_bikes(request, blocked_station.pk)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_blocked_stations_detail_bikes_tech_status(self, factory, blocked_station, tech):
        request = factory.get(f'/api/stations/{blocked_station.pk}/bikes')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = stations_detail_bikes(request, blocked_station.pk)
        assert response.status_code == status.HTTP_200_OK

    def test_get_blocked_stations_detail_bikes_admin_status(self, factory, blocked_station, admin):
        request = factory.get(f'/api/stations/{blocked_station.pk}/bikes')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_detail_bikes(request, blocked_station.pk)
        assert response.status_code == status.HTTP_200_OK

    def test_get_non_existing_stations_detail_bikes_user_status(self, factory, user):
        request = factory.get('/api/stations/2137/bikes')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = stations_detail_bikes(request, 2137)
        assert response.status_code == status.HTTP_404_NOT_FOUND
