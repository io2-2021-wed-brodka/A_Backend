import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, BikeStation
from BikeRentalApi.views import stations_detail


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
    def admin(self):
        user = User.objects.create(
            username = 'Pawel', first_name = 'Pawel', last_name = 'Tester', email = 'Pawel@test.com',
            password = 'test1234')
        return models.Admin.objects.create(user = user)

    @pytest.fixture
    def station(self):
        return BikeStation.objects.create(name = 'Test station', state = StationState.Blocked)

    @pytest.fixture
    def working_station(self):
        return BikeStation.objects.create(name = 'Test station', state = StationState.Working)

    @pytest.fixture
    def empty_station(self):
        return BikeStation.objects.create(name = 'Empty station', state = StationState.Blocked)

    @pytest.fixture
    def bike(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Working)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_get_stations_detail_user_status(self, factory, station, user):
        request = factory.get(f'/api/stations/{station.pk}')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = stations_detail(request, station.pk)
        assert response.status_code == status.HTTP_200_OK

    def test_get_stations_detail_tech_status(self, factory, station, tech):
        request = factory.get(f'/api/stations/{station.pk}')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = stations_detail(request, station.pk)

        assert response.status_code == status.HTTP_200_OK

    def test_get_stations_detail_admin_status(self, factory, station, admin):
        request = factory.get(f'/api/stations/{station.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_detail(request, station.pk)

        assert response.status_code == status.HTTP_200_OK

    def test_get_stations_detail_response(self, factory, station, user):
        request = factory.get(f'/api/stations/{station.pk}')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = stations_detail(request, station.pk)

        assert json.loads(response.content) == {
            'id': str(station.pk),
            'name': station.name,
            'status': station.state.label,
            'activeBikesCount': Bike.objects.filter(station__pk = station.pk, bike_state = BikeState.Working).count()
        }

    def test_delete_stations_detail_user_status(self, factory, station, user):
        request = factory.delete(f'/api/stations/{station.pk}')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = stations_detail(request, station.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_stations_detail_tech_status(self, factory, station, tech):
        request = factory.delete(f'/api/stations/{station.pk}')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = stations_detail(request, station.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_stations_detail_admin_status(self, factory, station, admin):
        request = factory.delete(f'/api/stations/{station.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_detail(request, station.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_stations_detail_admin_bad_request(self, factory, admin):
        request = factory.delete(f'/api/bikes/{420}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_detail(request, 420)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_stations_detail_admin_working_station(self, factory, admin, working_station):
        request = factory.delete(f'/api/stations/{working_station.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_detail(request, working_station.pk)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_stations_detail_admin_not_empty(self, factory, station, bike, admin):
        request = factory.delete(f'/api/stations/{station.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = stations_detail(request, station.pk)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
