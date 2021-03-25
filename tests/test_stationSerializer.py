import pytest

from BikeRentalApi.enums import StationState
from BikeRentalApi.models import BikeStation
from BikeRentalApi.serializers.stationSerializer import StationSerializer


@pytest.fixture
def station():
    return BikeStation(location_name = 'Testowa stacja', state = StationState.Working)


@pytest.fixture
def serialized_station(station):
    return StationSerializer(station).data


def test_contains_expected_fields(serialized_station):
    assert set(serialized_station.keys()) == {'id', 'location_name'}


def test_bike_state_field_content(serialized_station, station):
    assert serialized_station['location_name'] == station.location_name
