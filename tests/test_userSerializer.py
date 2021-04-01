import pytest

from BikeRentalApi.models import User
from BikeRentalApi.serializers.userSerializer import UserSerializer


@pytest.mark.django_db
class TestUserSerializer:
    @pytest.fixture
    def user(self):
        return User.objects.create(name = 'Jan', last_name = 'Kowalski')

    @pytest.fixture
    def serialized_user(self, user):
        return UserSerializer(user).data

    def test_contains_expected_fields(self, serialized_user):
        assert set(serialized_user.keys()) == {'id', 'name'}

    def test_name_field_content(self, serialized_user, user):
        assert serialized_user['name'] == user.name
