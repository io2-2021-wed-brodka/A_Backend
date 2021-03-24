import pytest

from BikeRentalApi.enums import StationState
from BikeRentalApi.models import BikeStation
from BikeRentalApi.serializers.stationSerializer import StationSerializer


@pytest.fixture
def station():
    return BikeStation(location_name='Testowa stacja', state=StationState.Working)


def test_station_serializer(station):
    serialized_station = StationSerializer(station).data
    assert serialized_station.__str__() == "{'id': None, 'location_name': 'Testowa stacja'}"
