import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework.exceptions import PermissionDenied

from BikeRentalApi.authentication import authenticate
from BikeRentalApi.models import Tech


@pytest.mark.django_db
class TestAuthentication:

    @pytest.fixture
    def user(self):
        return User.objects.create(
            username = 'Mariusz', first_name = 'Mariusz', last_name = 'Tester', email = 'mariusz@test.com',
            password = 'test123'
        )

    @pytest.fixture
    def authenticated_request(self, user):
        rq = RequestFactory().get('/api')
        rq.user = user
        return rq

    def test_raises_permission_denied_for_user_not_int_db(self, authenticated_request, user):
        with pytest.raises(PermissionDenied):
            authenticate(authenticated_request)

    def test_returns_authorized_user(self, authenticated_request, user):
        tech = Tech.objects.create(name = user.username, last_name = user.last_name)
        auth_user = authenticate(authenticated_request)
        assert auth_user == tech
