import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, BikeStation
from BikeRentalApi.views import bikes_blocked


@pytest.mark.django_db
class TestBikesListViews:

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
    def bike_working(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Working)

    @pytest.fixture
    def bike_blocked(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Blocked)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_get_bikes_list_user_status(self, factory, user):
        request = factory.get('/api/bikes/blocked')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = bikes_blocked(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_bikes_list_tech_status(self, factory, tech):
        request = factory.get('/api/bikes/blocked')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = bikes_blocked(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_bikes_list_tech_body(self, factory, user, station, bike_blocked, tech):
        request = factory.get('/api/bikes/blocked')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = bikes_blocked(request)
        assert json.loads(response.content) == [
            {
                'id': bike_blocked.pk,
                'station': {
                    'id': station.pk,
                    'name': 'Test station'
                },
                'bike_state': BikeState.Blocked,
                'user': None
            }
        ]

    def test_post_bikes_list_user_status(self, factory, bike_working, user):
        body = json.dumps({'id': bike_working.id})
        request = factory.post('/api/bikes/blocked', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_blocked(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_bikes_list_tech_status(self, factory, bike_working, tech):
        body = json.dumps({'id': bike_working.id})
        request = factory.post('/api/bikes/blocked', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {tech.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_blocked(request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_bikes_list_tech_response(self, factory, bike_working, station, tech):
        body = json.dumps({'id': bike_working.pk})
        request = factory.post('/api/bikes/blocked', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {tech.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_blocked(request)
        data = json.loads(response.content)

        assert data['id'] == bike_working.id \
               and data['station'] == {"id": station.pk, "name": station.name} \
               and data['bike_state'] == BikeState.Blocked \
               and data['user'] is None \
               and set(data.keys()) == {'id', 'station', 'bike_state', 'user'}

    def test_post_bikes_tech_list_bad_request_status(self, factory, tech):
        body = json.dumps({'id': 2137})
        request = factory.post('/api/bikes/blocked', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {tech.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_blocked(request)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_bikes_list_tech_bad_bike(self, factory, bike_blocked, station, tech):
        body = json.dumps({'id': bike_blocked.pk})
        request = factory.post('/api/bikes/blocked', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {tech.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_blocked(request)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



    def test_post_bikes_list_admin_status(self, factory, bike_working, admin):
        body = json.dumps({'id': bike_working.id})
        request = factory.post('/api/bikes/blocked', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_blocked(request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_bikes_list_admin_response(self, factory, bike_working, station, admin):
        body = json.dumps({'id': bike_working.pk})
        request = factory.post('/api/bikes/blocked', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_blocked(request)
        data = json.loads(response.content)

        assert data['id'] == bike_working.id \
               and data['station'] == {"id": station.pk, "name": station.name} \
               and data['bike_state'] == BikeState.Blocked \
               and data['user'] is None \
               and set(data.keys()) == {'id', 'station', 'bike_state', 'user'}

    def test_post_bikes_admin_list_bad_request_status(self, factory, admin):
        body = json.dumps({'id': 2137})
        request = factory.post('/api/bikes/blocked', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_blocked(request)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_bikes_list_admin_bad_bike(self, factory, bike_blocked, station, admin):
        body = json.dumps({'id': bike_blocked.pk})
        request = factory.post('/api/bikes/blocked', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_blocked(request)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY