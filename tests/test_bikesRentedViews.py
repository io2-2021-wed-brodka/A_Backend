from datetime import date, time, datetime, timedelta

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from A_Backend.common_settings import BIKE_RENTAL_LIMIT
from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, Rental, BikeStation, Reservation
from BikeRentalApi.views import bikes_rented


@pytest.mark.django_db
class TestBikesRentedViews:

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
    def user_with_limit(self, station):
        user = User.objects.create(
            username = 'Bartosz', first_name = 'Bartosz', last_name = 'Tester', email = 'Bartosz@test.com',
            password = 'test1234')
        user = models.AppUser.objects.create(user = user)
        for i in range(BIKE_RENTAL_LIMIT):
            bike = Bike.objects.create(station = None, bike_state = BikeState.InService)
            Rental.objects.create(user_id = user.pk, start_date = timezone.now(), bike_id = bike.id)
        return user

    @pytest.fixture
    def bike1(self, user, station):
        bike = Bike.objects.create(station = None, bike_state = BikeState.InService)
        rental_date = date(2005, 7, 14)
        rental_start_time = time(12, 30)
        rental_start_datetime = datetime.combine(rental_date, rental_start_time, tzinfo = timezone.utc)
        Rental.objects.create(user = user, bike = bike, start_date = rental_start_datetime)
        return bike

    @pytest.fixture
    def bike2(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Working)

    @pytest.fixture
    def bike3(self, user, station):
        bike = Bike.objects.create(station = station, bike_state = BikeState.Reserved)
        start_date = timezone.now()
        Reservation.objects.create(bike = bike, user = user, start_date = start_date,
                                   expire_date = start_date + timedelta(minutes = 3))
        return bike

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_get_bikes_rented_status_user(self, user, factory):
        request = factory.get('/api/bikes/rented')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = bikes_rented(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_bikes_rented_status_tech(self, tech, factory):
        request = factory.get('/api/bikes/rented')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = bikes_rented(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_bikes_rented_status_admin(self, admin, factory):
        request = factory.get('/api/bikes/rented')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = bikes_rented(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_bikes_rented_response(self, user, factory, bike1, station):
        request = factory.get('/api/bikes/rented')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = bikes_rented(request)
        assert json.loads(response.content) == {
            "bikes": [
                {
                    'id': str(bike1.pk),
                    'station': None,
                    'status': BikeState.InService.label,
                    'user': {
                        'id': str(user.pk),
                        'name': user.user.first_name
                    }
                }
            ]
        }

    def test_post_bikes_rented_user_status(self, user, bike2, factory):
        body = json.dumps({"id": str(bike2.pk)})
        request = factory.post('api/bikes/rented', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_rented(request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_bikes_rented_bad_request(self, user, factory):
        body = json.dumps({"id": '1337'})
        request = factory.post('api/bikes/rented', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_rented(request)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_bikes_rented_bike_user_reserved_by_user(self, user, bike3, factory):
        body = json.dumps({"id": str(bike3.pk)})
        request = factory.post('api/bikes/rented', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_rented(request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_bikes_rented_bike_tech_reserved_by_user(self, tech, bike3, factory):
        body = json.dumps({"id": str(bike3.pk)})
        request = factory.post('api/bikes/rented', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {tech.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_rented(request)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_post_bikes_rented_response(self, user, station, bike2, factory):
        body = json.dumps({"id": str(bike2.pk)})
        request = factory.post('api/bikes/rented', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_rented(request)
        assert json.loads(response.content) == {
            'id': str(bike2.pk),
            'station': None,
            'status': BikeState.InService.label,
            'user': {
                'id': str(user.pk),
                'name': user.user.first_name
            }
        }

    def test_post_bikes_rented_limit_reached_status(self, user_with_limit, station, bike2, factory):
        body = json.dumps({"id": str(bike2.pk)})
        request = factory.post('api/bikes/rented', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user_with_limit.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_rented(request)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_post_bikes_rented_limit_reached_response(self, user_with_limit, station, bike2, factory):
        body = json.dumps({"id": str(bike2.pk)})
        request = factory.post('api/bikes/rented', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user_with_limit.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = bikes_rented(request)
        assert set(json.loads(response.content).keys()) == {'message'}
