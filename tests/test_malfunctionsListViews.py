import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, BikeStation, Malfunction
from BikeRentalApi.views import bikes_list, malfunctions_list


@pytest.mark.django_db
class TestMalfunctionsListViews:

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
    def station(self):
        return BikeStation.objects.create(name = 'Test station', state = StationState.Working)

    @pytest.fixture
    def bike(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Working)

    @pytest.fixture
    def reporting_user(self):
        user = User.objects.create(
            username = 'reporter', first_name = 'Reporting', last_name = 'Reporter', email = 'reporter@test.com',
            password = 'test1234')
        return models.AppUser.objects.create(user = user)

    @pytest.fixture
    def malfunction(self, bike, reporting_user):
        return Malfunction.objects.create(bike = bike, description = 'Broken', reporting_user = reporting_user.user)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_get_bikes_list_user_status(self, factory, user):
        request = factory.get('/api/malfunctions')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = bikes_list(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_bikes_list_tech_status(self, factory, tech):
        request = factory.get('/api/malfunctions')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = bikes_list(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_bikes_list_tech_body(self, factory, user, station, bike, tech, malfunction):
        request = factory.get('api/malfunctions')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = malfunctions_list(request)
        assert json.loads(response.content) == {
            "malfunctions": [
                {
                    'id': str(malfunction.pk),
                    'bikeId': str(malfunction.bike_id),
                    'description': malfunction.description,
                    'reportingUserId': str(malfunction.reporting_user_id)
                }
            ]
        }
