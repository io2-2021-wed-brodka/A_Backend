import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, BikeStation
from BikeRentalApi.views import stations_active


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
    def station_working(self):
        return BikeStation.objects.create(name = 'Test working station', state = StationState.Working)

    @pytest.fixture
    def bike(self, station_working):
        return Bike.objects.create(station = station_working, status = BikeState.Working)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_get_stations_active_user_status(self, factory, user):
        request = factory.get('/api/stations/blocked')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = stations_active(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_stations_active_tech_status(self, factory, tech):
        request = factory.get('/api/stations/blocked')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = stations_active(request)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_stations_active_admin_status(self, factory, admin):
        request = factory.get('/api/stations/blocked')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_active(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_stations_active_response(self, admin, factory, station_working):
        request = factory.get('/api/stations/blocked')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_active(request)
        assert json.loads(response.content) == [
            {
                'id': str(station_working.pk),
                'name': station_working.name,
                'status': station_working.state.label,
                'activeBikesCount': Bike.objects.filter(station__pk = station_working.pk, bike_state = BikeState.Working).count()
            }
        ]
