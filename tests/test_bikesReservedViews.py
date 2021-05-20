from datetime import datetime, timedelta

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState, UserState
from BikeRentalApi.models import Bike, BikeStation, Reservation
from BikeRentalApi.views import bikes_reserved


@pytest.mark.django_db
class TestBikesReservedViews:

    @pytest.fixture
    def user(self):
        user = User.objects.create(
            username = 'Janek', first_name = 'Janek', last_name = 'Tester', email = 'Janek@test.com',
            password = 'test1234')
        return models.AppUser.objects.create(user = user)

    @pytest.fixture
    def blocked_user(self):
        user = User.objects.create(
            username = 'Blocked', first_name = 'Blocked', last_name = 'Tester', email = 'blocked@test.com',
            password = 'test1234')
        return models.AppUser.objects.create(user = user, state = UserState.Banned)

    @pytest.fixture
    def tech(self):
        tech = User.objects.create(
            username = 'Mariusz', first_name = 'Mariusz', last_name = 'Tester', email = 'mariusz@test.com',
            password = 'test123')
        return models.Tech.objects.create(user = tech)

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
    def bike_reserved(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Reserved)

    @pytest.fixture
    def reservation(self, user, bike_reserved):
        start_date = timezone.now()
        return Reservation.objects.create(user = user, bike = bike_reserved, start_date = start_date,
                                          expire_date = start_date + timedelta(minutes = 3))

    @pytest.fixture
    def bike_free(self, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Working)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_get_bikes_reserved_status_user(self, user, factory):
        request = factory.get('/api/bikes/reserved')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = bikes_reserved(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_bikes_reserved_status_tech(self, tech, factory):
        request = factory.get('/api/bikes/reserved')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = bikes_reserved(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_bikes_reserved_status_admin(self, admin, factory):
        request = factory.get('/api/bikes/reserved')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = bikes_reserved(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_bikes_reserved_response(self, user, factory, bike_reserved, station, reservation):
        request = factory.get('/api/bikes/reserved')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = bikes_reserved(request)
        assert json.loads(response.content) == {
            "bikes": [
                {
                    'id': str(bike_reserved.pk),
                    'station': {
                        'id': str(station.pk),
                        'name': station.name,
                        'status': StationState.Working.label,
                        'activeBikesCount': 0
                    },
                    'reservedAt': reservation.start_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    'reservedTill': reservation.expire_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                }
            ]
        }

    def test_post_bikes_reserved_user_status(self, user, bike_free, factory):
        body = json.dumps({"id": str(bike_free.pk)})
        request = factory.post('api/bikes/reserved', content_type = 'application/json', data = body)

        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_reserved(request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_bikes_reserved_response(self, user, station, bike_free, factory):
        body = json.dumps({"id": str(bike_free.pk)})
        request = factory.post('api/bikes/reserved', content_type = 'application/json', data = body)

        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_reserved(request)
        content = json.loads(response.content)

        assert isinstance(datetime.strptime(content['reservedAt'], '%Y-%m-%dT%H:%M:%S.%fZ'), datetime) and \
            isinstance(datetime.strptime(content['reservedTill'], '%Y-%m-%dT%H:%M:%S.%fZ'), datetime) and \
            content['id'] == str(bike_free.pk) and \
            content['station'] == {
                'id': str(station.pk),
                'name': station.name,
                'status': StationState.Working.label,
                'activeBikesCount': 0
            }

    def test_post_bikes_reserved_bad_request(self, user, factory):
        body = json.dumps({"id": '1337'})
        request = factory.post('api/bikes/reserved', content_type = 'application/json', data = body)

        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_reserved(request)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_bikes_reserved_bike_already_taken_status(self, tech, bike_reserved, factory):
        body = json.dumps({"id": str(bike_reserved.pk)})
        request = factory.post('api/bikes/reserved', content_type = 'application/json', data = body)

        headers = {'Authorization': f'Bearer {tech.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_reserved(request)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_post_bikes_reserved_bike_already_taken_response(self, tech, bike_reserved, factory):
        body = json.dumps({"id": str(bike_reserved.pk)})
        request = factory.post('api/bikes/reserved', content_type = 'application/json', data = body)

        headers = {'Authorization': f'Bearer {tech.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_reserved(request)
        assert set(json.loads(response.content).keys()) == {'message'}

    def test_post_bikes_reserved_user_blocked_status(self, blocked_user, bike_free, factory):
        body = json.dumps({"id": str(bike_free.pk)})
        request = factory.post('api/bikes/reserved', content_type = 'application/json', data = body)

        headers = {'Authorization': f'Bearer {blocked_user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_reserved(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_bikes_reserved_user_blocked_response_headers(self, blocked_user, bike_free, factory):
        body = json.dumps({"id": str(bike_free.pk)})
        request = factory.post('api/bikes/reserved', content_type = 'application/json', data = body)

        headers = {'Authorization': f'Bearer {blocked_user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_reserved(request)
        assert set(json.loads(response.content).keys()) == {'message'}
