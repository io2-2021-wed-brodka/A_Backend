from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import Bike, BikeStation, Reservation
from BikeRentalApi.jobs.minutely import clear_expired_reservations


@pytest.mark.django_db
class TestClearExpiredReservationsJob:

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
    def bike_reserved(self, user, station):
        return Bike.objects.create(station = station, bike_state = BikeState.Reserved)

    @pytest.fixture
    def valid_reservation(self, user, bike_reserved):
        start_date = timezone.now()
        return Reservation.objects.create(user = user, bike = bike_reserved,
                                          start_date = start_date - timedelta(minutes = 2),
                                          expire_date = start_date + timedelta(minutes = 2))

    @pytest.fixture
    def expired_reservation(self, user, bike_reserved):
        start_date = timezone.now()
        return Reservation.objects.create(user = user, bike = bike_reserved,
                                          start_date = start_date - timedelta(minutes = 2),
                                          expire_date = start_date - timedelta(minutes = 1))

    def test_cleared_expired_reservation(self, user, bike_reserved, expired_reservation):
        pre_job = Reservation.objects.count()
        job = clear_expired_reservations.Job()
        job.execute()
        post_job = Reservation.objects.count()
        assert post_job == pre_job - 1

    def test_cleared_expired_reservation_bike_status(self, user, bike_reserved, expired_reservation):
        job = clear_expired_reservations.Job()
        job.execute()
        bike = Bike.objects.get(pk = bike_reserved.pk)
        assert bike.bike_state == BikeState.Working

    def test_valid_reservation_not_cleared(self, user, bike_reserved, valid_reservation):
        pre_job = Reservation.objects.count()
        job = clear_expired_reservations.Job()
        job.execute()
        post_job = Reservation.objects.count()
        assert post_job == pre_job

    def test_valid_reservation_bike_status(self, user, bike_reserved, valid_reservation):
        job = clear_expired_reservations.Job()
        job.execute()
        bike = Bike.objects.get(pk = bike_reserved.pk)
        assert bike.bike_state == BikeState.Reserved
