import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework.exceptions import PermissionDenied

from BikeRentalApi.authentication import authenticate


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
