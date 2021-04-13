import pytest
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, BikeStation
from BikeRentalApi.views import bikes_detail


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
    def bike2(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Working)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_delete_bikes_detail_user_status(self, factory, bike, user):
        request = factory.delete(f'/api/bikes/{bike.pk}')
        request.user = user.user

        response = bikes_detail(request, bike.pk)
        assert response.status_code == 401

    def test_delete_bikes_detail_tech_status(self, factory, bike, tech):
        request = factory.delete(f'/api/bikes/{bike.pk}')
        request.user = tech.user

        response = bikes_detail(request, bike.pk)

        assert response.status_code == 401

    def test_delete_bikes_detail_admin_status(self, factory, bike, admin):
        request = factory.delete(f'/api/bikes/{bike.pk}')
        request.user = admin.user

        response = bikes_detail(request, bike.pk)

        assert response.status_code == 200

    def test_delete_bikes_detail_admin_bad_request(self, factory, admin):
        request = factory.delete(f'/api/bikes/{420}')
        request.user = admin.user

        with pytest.raises(Http404):
            response = bikes_detail(request, 420)

    def test_delete_bikes_detail_admin_response(self, factory, bike2, admin):
        request = factory.delete(f'/api/bikes/{bike2.pk}')
        request.user = admin.user

        response = bikes_detail(request, bike2.pk)

        assert json.loads(response.content) == {
            'id': 8,
            'station': {
                'id': 8,
                'name': 'Test station'
            },
            'bike_state': 0,
            'user': None
        }
