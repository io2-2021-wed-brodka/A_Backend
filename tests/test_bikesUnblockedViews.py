import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, BikeStation
from BikeRentalApi.views import bikes_unblocked


@pytest.mark.django_db
class TestBikesUnblockedViews:

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
    def bike_blocked(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Blocked)

    @pytest.fixture
    def bike_working(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Working)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_delete_bikes_unblock_user_status(self, factory, bike_blocked, user):
        request = factory.delete(f'/api/bikes/blocked/{bike_blocked.pk}')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = bikes_unblocked(request, bike_blocked.pk)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_bikes_unblock_tech_status(self, factory, bike_blocked, tech):
        request = factory.delete(f'/api/bikes/blocked/{bike_blocked.pk}')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = bikes_unblocked(request, bike_blocked.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_bikes_unblock_tech_bad_request(self, factory, tech):
        request = factory.delete(f'/api/bikes/blocked/{420}')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = bikes_unblocked(request, 420)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_bikes_unblock_tech_not_blocked(self, factory, bike_working, tech):
        request = factory.delete(f'/api/bikes/blocked/{bike_working.pk}')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = bikes_unblocked(request, bike_working.pk)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_bikes_unblock_admin_status(self, factory, bike_blocked, admin):
        request = factory.delete(f'/api/bikes/blocked/{bike_blocked.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = bikes_unblocked(request, bike_blocked.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_bikes_unblock_admin_bad_request(self, factory, admin):
        request = factory.delete(f'/api/bikes/blocked/{420}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = bikes_unblocked(request, 420)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_bikes_unblock_admin_not_blocked(self, factory, bike_working, admin):
        request = factory.delete(f'/api/bikes/blocked/{bike_working.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = bikes_unblocked(request, bike_working.pk)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
