import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, BikeStation
from BikeRentalApi.views import bikes_list


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
    def bike(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Working)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_get_bikes_list_user_status(self, factory, user):
        request = factory.get('/api/bikes')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = bikes_list(request)
        assert response.status_code == 401

    def test_get_bikes_list_tech_status(self, factory, tech):
        request = factory.get('/api/bikes')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = bikes_list(request)

        assert response.status_code == 200

    def test_get_bikes_list_tech_body(self, factory, user, station, bike, tech):
        request = factory.get('api/bikes')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = bikes_list(request)

        assert json.loads(response.content) == [
            {
                'id': bike.pk,
                'station': {
                    'id': station.pk,
                    'name': 'Test station'
                },
                'bike_state': BikeState.Working,
                'user': None
            }
        ]

    def test_post_bikes_list_user_status(self, factory, station, user):
        body = json.dumps({'id': station.id})
        request = factory.post('/api/bikes', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_list(request)

        assert response.status_code == 401

    def test_post_bikes_list_tech_status(self, factory, station, tech):
        body = json.dumps({'id': station.id})
        request = factory.post('/api/bikes', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {tech.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_list(request)

        assert response.status_code == 401

    def test_post_bikes_list_admin_status(self, factory, station, admin):
        body = json.dumps({'id': station.id})
        request = factory.post('/api/bikes', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_list(request)

        assert response.status_code == 201

    def test_post_bikes_list_admin_response(self, factory, station, admin):
        body = json.dumps({'id': station.pk})
        request = factory.post('/api/bikes', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_list(request)
        data = json.loads(response.content)

        assert isinstance(data['id'], int) \
               and data['station'] == {"id": station.pk, "name": station.name} \
               and data['bike_state'] == BikeState.Working \
               and data['user'] is None \
               and set(data.keys()) == {'id', 'station', 'bike_state', 'user'}

    def test_post_bikes_list_bad_request_status(self, factory, admin):
        body = json.dumps({'id': 2137})
        request = factory.post('/api/bikes', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_list(request)

        assert response.status_code == 404
