import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework.exceptions import PermissionDenied

from BikeRentalApi.authentication import authenticate
from BikeRentalApi.models import Tech


@pytest.mark.django_db
class TestAuthentication:

    @pytest.fixture
    def auth_user(self):
        return User.objects.create(
            username = 'Mariusz', first_name = 'Mariusz', last_name = 'Tester', email = 'mariusz@test.com',
            password = 'test123'
        )

    @pytest.fixture
    def authenticated_request(self, auth_user):
        rq = RequestFactory().get('/api')
        rq.headers = {'Authorization': f'Bearer {auth_user.username}'}
        return rq

    def test_raises_permission_denied_for_user_not_int_db(self, authenticated_request, auth_user):
        with pytest.raises(PermissionDenied):
            authenticate(authenticated_request)

    def test_returns_authorized_user(self, authenticated_request, auth_user):
        tech = Tech.objects.create(user = auth_user)
        target_user = authenticate(authenticated_request)
        assert target_user == tech
