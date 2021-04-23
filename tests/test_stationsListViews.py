import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, BikeStation
from BikeRentalApi.views import stations_list


@pytest.mark.django_db
class TestStationsListViews:

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

    def test_get_stations_list_user_status(self, factory, user):
        request = factory.get('/api/stations')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = stations_list(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_stations_list_tech_status(self, factory, tech):
        request = factory.get('/api/stations')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = stations_list(request)

        assert response.status_code == status.HTTP_200_OK

    def test_get_stations_list_admin_status(self, factory, admin):
        request = factory.get('/api/stations')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_list(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_stations_list_response(self, user, factory, station):
        request = factory.get('/api/stations')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = stations_list(request)
        assert json.loads(response.content) == [
            {
                'id': station.pk,
                'name': station.name,
                'status': station.state.label,
                'activeBikesCount': Bike.objects.filter(station__pk = station.pk, bike_state = BikeState.Working).count()
            }
        ]

    def test_post_stations_list_user_status(self, factory, user):
        body = json.dumps({'name': 'New station'})
        request = factory.post('/api/stations', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = stations_list(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_stations_list_tech_status(self, factory, tech):
        body = json.dumps({'name': 'New station'})
        request = factory.post('/api/stations', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {tech.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = stations_list(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_stations_list_admin_status(self, factory, admin):
        body = json.dumps({'name': 'New station'})
        request = factory.post('/api/stations', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = stations_list(request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_stations_list_admin_response(self, factory, admin):
        name = 'New station'
        body = json.dumps({'name': name})
        request = factory.post('/api/stations', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = stations_list(request)
        data = json.loads(response.content)

        assert isinstance(data['id'], int) and data['name'] == name and set(data.keys()) == {'id', 'name', 'status', 'activeBikesCount'}
