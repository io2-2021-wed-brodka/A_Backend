from datetime import date, time, datetime

from django.contrib.auth.models import User
from django.utils import timezone

import pytest

from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import BikeStation, Bike, Rental, AppUser
from BikeRentalApi.serializers.bikeSerializer import BikeSerializer
from BikeRentalApi.serializers.stationSerializer import StationSerializer
from BikeRentalApi.serializers.userSerializer import UserSerializer


@pytest.mark.django_db
class TestBikeSerializer:
    @pytest.fixture()
    def user(self):
        user = User.objects.create(
            username = 'Mariusz', first_name = 'Mariusz', last_name = 'Tester', email = 'mariusz@test.com',
            password = 'test123'
        )
        return AppUser.objects.create(user = user)

    @pytest.fixture()
    def bike(self, user):
        station = BikeStation.objects.create(name = 'Test station', state = StationState.Working)
        bike = Bike.objects.create(station = station, bike_state = BikeState.Working)
        rental_date = date(2005, 7, 14)
        rental_start_time = time(12, 30)
        rental_start_datetime = datetime.combine(rental_date, rental_start_time, tzinfo = timezone.utc)
        Rental.objects.create(user = user, bike = bike, start_date = rental_start_datetime)
        return bike

    @pytest.fixture()
    def bike_serializer(self, bike):
        return BikeSerializer(bike)

    @pytest.fixture()
    def serialized_bike(self, bike_serializer):
        return bike_serializer.data

    def test_contains_expected_fields(self, serialized_bike):
        assert set(serialized_bike.keys()) == {'id', 'status', 'station', 'user'}

    def test_bike_state_field_content(self, serialized_bike, bike):
        assert serialized_bike['status'] == bike.bike_state.label

    def test_station_field_content(self, serialized_bike, bike):
        assert serialized_bike['station'] == StationSerializer(bike.station).data

    def test_user_field_content(self, serialized_bike, user):
        assert serialized_bike['user'] == UserSerializer(user).data
