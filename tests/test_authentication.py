import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import PermissionDenied, NotAuthenticated, AuthenticationFailed

from BikeRentalApi.authentication import authenticate_bikes_user
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
    def unauthorized_request(self):
        return APIRequestFactory().get('/api')

    @pytest.fixture
    def authenticated_request(self, unauthorized_request, auth_user):
        unauthorized_request.headers = {'Authorization': f'Bearer {auth_user.username}'}
        return unauthorized_request

    def test_raises_permission_denied_for_user_not_int_db(self, authenticated_request, unauthorized_request, auth_user):
        with pytest.raises(PermissionDenied):
            authenticate_bikes_user(authenticated_request)

    def test_raises_not_authenticated_for_lacking_auth_header(self, unauthorized_request):
        with pytest.raises(NotAuthenticated):
            authenticate_bikes_user(unauthorized_request)

    def test_raises_authentication_failed_for_invalid_auth_header(self, unauthorized_request):
        unauthorized_request.headers = {'Authorization': 'invalid'}
        with pytest.raises(AuthenticationFailed):
            authenticate_bikes_user(unauthorized_request)

    def test_returns_authorized_user(self, authenticated_request, auth_user):
        tech = Tech.objects.create(user = auth_user)
        target_user = authenticate_bikes_user(authenticated_request)
        assert target_user == tech
