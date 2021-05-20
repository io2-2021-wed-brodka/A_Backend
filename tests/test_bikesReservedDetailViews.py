from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, BikeStation, Reservation
from BikeRentalApi.views import bikes_reserved_detail


@pytest.mark.django_db
class TestBikesReservedDetailViews:

    @pytest.fixture
    def user(self):
        user = User.objects.create(
            username = 'Janek', first_name = 'Janek', last_name = 'Tester', email = 'Janek@test.com',
            password = 'test1234')
        return models.AppUser.objects.create(user = user)

    @pytest.fixture
    def tech(self):
        tech = User.objects.create(
            username = 'Mariusz', first_name = 'Mariusz', last_name = 'Tester', email = 'mariusz@test.com',
            password = 'test123')
        return models.Tech.objects.create(user = tech)

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
    def bike_reserved(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Reserved)

    @pytest.fixture
    def reservation_user(self, user, bike_reserved):
        start_date = timezone.now()
        return Reservation.objects.create(user = user, bike = bike_reserved, start_date = start_date,
                                          expire_date = start_date + timedelta(minutes = 3))

    @pytest.fixture
    def reservation_tech(self, tech, bike_reserved):
        start_date = timezone.now()
        return Reservation.objects.create(user = tech, bike = bike_reserved, start_date = start_date,
                                          expire_date = start_date + timedelta(minutes = 3))

    @pytest.fixture
    def reservation_admin(self, admin, bike_reserved):
        start_date = timezone.now()
        return Reservation.objects.create(user = admin, bike = bike_reserved, start_date = start_date,
                                          expire_date = start_date + timedelta(minutes = 3))

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_delete_reservation_detail_user_status(self, factory, reservation_user, user, bike_reserved):
        request = factory.delete(f'/api/bikes/reserved/{bike_reserved.pk}')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = bikes_reserved_detail(request, bike_reserved.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_reservation_detail_tech_status(self, factory, reservation_tech, tech, bike_reserved):
        request = factory.delete(f'/api/bikes/reserved/{bike_reserved.pk}')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = bikes_reserved_detail(request, bike_reserved.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_reservation_detail_admin_status(self, factory, reservation_admin, admin, bike_reserved):
        request = factory.delete(f'/api/bikes/reserved/{bike_reserved.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = bikes_reserved_detail(request, bike_reserved.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_reservation_detail_nonexisting_bike_status(self, factory, reservation_admin, bike_reserved, admin):
        request = factory.delete(f'/api/bikes/reserved/{bike_reserved.pk + 1}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = bikes_reserved_detail(request, bike_reserved.pk + 1)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_reservation_detail_nonexisting_bike_headers(self, factory, bike_reserved, admin):
        request = factory.delete(f'/api/bikes/reserved/{bike_reserved.pk + 1}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = bikes_reserved_detail(request, bike_reserved.pk + 1)
        assert set(json.loads(response.content).keys()) == {'message'}

    def test_delete_reservation_detail_bike_taken_status(self, factory, reservation_admin, bike_reserved, user):
        request = factory.delete(f'/api/bikes/reserved/{bike_reserved.pk}')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = bikes_reserved_detail(request, bike_reserved.pk)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_reservation_detail_bike_taken_headers(self, factory, reservation_admin, bike_reserved, user):
        request = factory.delete(f'/api/bikes/reserved/{bike_reserved.pk}')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = bikes_reserved_detail(request, bike_reserved.pk)
        assert set(json.loads(response.content).keys()) == {'message'}
