from datetime import date, time, datetime, timezone

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, BikeStation, Malfunction, Rental
from BikeRentalApi.views import malfunctions_list


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
    def rented_bike(self, user, station):
        bike = Bike.objects.create(station = None, bike_state = BikeState.InService)
        rental_date = date(2005, 7, 14)
        rental_start_time = time(12, 30)
        rental_start_datetime = datetime.combine(rental_date, rental_start_time, tzinfo = timezone.utc)
        Rental.objects.create(user = user, bike = bike, start_date = rental_start_datetime)
        return bike

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

        response = malfunctions_list(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_bikes_list_tech_status(self, factory, tech):
        request = factory.get('/api/malfunctions')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = malfunctions_list(request)
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

    def test_post_malfunctions_list_user_rented_status(self, factory, user, rented_bike):
        description = 'description'
        data = json.dumps({
            'id': rented_bike.id,
            'description': description
        })

        request = factory.post('/api/malfunctions', content_type = 'application/json', data = data)
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = malfunctions_list(request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_malfunctions_list_user_not_rented_status(self, factory, user, bike):
        description = 'description'
        data = json.dumps({
            'id': bike.id,
            'description': description
        })

        request = factory.post('/api/malfunctions', content_type = 'application/json', data = data)
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = malfunctions_list(request)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_post_malfunctions_list_user_rented_response_headers(self, factory, user, rented_bike):
        description = 'description'
        data = json.dumps({
            'id': rented_bike.id,
            'description': description
        })

        request = factory.post('/api/malfunctions', content_type = 'application/json', data = data)
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = malfunctions_list(request)
        content = json.loads(response.content)
        assert set(content.keys()) == {'id', 'bikeId', 'description', 'reportingUserId'}

    def test_post_malfunctions_list_user_rented_response_content(self, factory, user, rented_bike):
        description = 'description'
        data = json.dumps({
            'id': rented_bike.id,
            'description': description
        })

        request = factory.post('/api/malfunctions', content_type = 'application/json', data = data)
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = malfunctions_list(request)
        content = json.loads(response.content)
        assert isinstance(content['id'], str) and \
            content['description'] == description and \
            content['bikeId'] == str(rented_bike.id) and \
            content['reportingUserId'] == str(user.user.id)
