import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import StationState
from BikeRentalApi.models import BikeStation
from BikeRentalApi.views import stations_blocked_detail


@pytest.mark.django_db
class TestBikesDetailViews:

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
    def station_blocked(self):
        return BikeStation.objects.create(name = 'Test blocked station', state = StationState.Blocked)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_delete_station_blocked_detail_user_status(self, factory, station_blocked, user):
        request = factory.delete(f'/api/stations/blocked/{station_blocked.pk}')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = stations_blocked_detail(request, station_blocked.pk)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_station_blocked_detail_tech_status(self, factory, station_blocked, tech):
        request = factory.delete(f'/api/stations/blocked/{station_blocked.pk}')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = stations_blocked_detail(request, station_blocked.pk)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_station_blocked_detail_admin_status(self, factory, station_blocked, admin):
        request = factory.delete(f'/api/stations/blocked/{station_blocked.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_blocked_detail(request, station_blocked.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_station_blocked_detail_admin_bad_request(self, factory, station_blocked, admin):
        request = factory.delete(f'/api/stations/blocked/{420}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_blocked_detail(request, 420)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'message' in json.loads(response.content).keys()

    def test_delete_station_blocked_on_working_detail_admin(self, factory, station_working, admin):
        request = factory.delete(f'/api/stations/blocked/{station_working.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_blocked_detail(request, station_working.pk)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_station_blocked_detail_admin_duplicate(self, factory, station_blocked, admin):
        request = factory.delete(f'/api/stations/blocked/{station_blocked.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_blocked_detail(request, station_blocked.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = stations_blocked_detail(request, station_blocked.pk)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
