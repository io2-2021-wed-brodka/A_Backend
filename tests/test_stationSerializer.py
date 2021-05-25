import pytest

from BikeRentalApi.enums import StationState
from BikeRentalApi.models import BikeStation
from BikeRentalApi.serializers.stationSerializer import StationSerializer


@pytest.mark.django_db
class TestStationSerializer:
    @pytest.fixture
    def station(self):
        return BikeStation.objects.create(name = 'Testowa stacja', state = StationState.Working)

    @pytest.fixture
    def serialized_station(self, station):
        return StationSerializer(station).data

    def test_contains_expected_fields(self, serialized_station):
        assert set(serialized_station.keys()) == {'id', 'name', 'status', 'activeBikesCount', 'bikesLimit'}

    def test_bike_state_field_content(self, serialized_station, station):
        assert serialized_station['name'] == station.name
