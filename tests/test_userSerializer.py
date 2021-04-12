import pytest

from django.contrib.auth.models import User

from BikeRentalApi.models import AppUser
from BikeRentalApi.serializers.userSerializer import UserSerializer


@pytest.mark.django_db
class TestUserSerializer:
    @pytest.fixture
    def user(self):
        user = User.objects.create(
            username = 'Mariusz', first_name = 'Mariusz', last_name = 'Tester', email = 'mariusz@test.com',
            password = 'test123'
        )
        return AppUser.objects.create(user = user)

    @pytest.fixture
    def serialized_user(self, user):
        return UserSerializer(user).data

    def test_contains_expected_fields(self, serialized_user):
        assert set(serialized_user.keys()) == {'id', 'name'}

    def test_name_field_content(self, serialized_user, user):
        assert serialized_user['name'] == user.user.first_name
