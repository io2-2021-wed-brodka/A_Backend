import pytest

from BikeRentalApi.models import User
from BikeRentalApi.serializers.userSerializer import UserSerializer


@pytest.fixture
def user():
    return User(name = 'Jan', last_name = 'Kowalski')


@pytest.fixture
def serialized_user(user):
    return UserSerializer(user).data


def test_contains_expected_fields(serialized_user):
    assert set(serialized_user.keys()) == {'id', 'name', 'last_name'}


def test_name_field_content(serialized_user, user):
    assert serialized_user['name'] == user.name


def test_last_name_field_content(serialized_user, user):
    assert serialized_user['last_name'] == user.last_name
