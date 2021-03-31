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
        assert set(serialized_user.keys()) == {'id', 'name', 'last_name', 'role', 'state'}

    def test_name_field_content(self, serialized_user, user):
        assert serialized_user['name'] == user.name

    def test_last_name_field_content(self, serialized_user, user):
        assert serialized_user['last_name'] == user.last_name
