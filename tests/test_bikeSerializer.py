import pytest

from BikeRentalApi.enums import BikeState, StationState
from BikeRentalApi.models import BikeStation, Bike
from BikeRentalApi.serializers.bikeSerializer import BikeSerializer
from BikeRentalApi.serializers.stationSerializer import StationSerializer


@pytest.fixture(autouse = True)
def bike():
    station = BikeStation(location_name = 'Test station', state = StationState.Working)
    return Bike(station = station, bike_state = BikeState.Working)


@pytest.fixture(autouse = True)
def bike_serializer(bike):
    return BikeSerializer(bike)


@pytest.fixture(autouse = True)
def serialized_bike(bike_serializer):
    return bike_serializer.data


def test_contains_expected_fields(serialized_bike):
    assert set(serialized_bike.keys()) == {'id', 'bike_state', 'station', 'user'}


def test_bike_state_field_content(serialized_bike, bike):
    assert serialized_bike['bike_state'] == bike.bike_state


def test_station_field_content(serialized_bike, bike):
    assert serialized_bike['station'] == StationSerializer(bike.station).data


def test_user_field_content(serialized_bike):
    assert serialized_bike['user'] is None
