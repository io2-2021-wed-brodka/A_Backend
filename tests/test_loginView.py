import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi.auth_views import login
from BikeRentalApi.models import AppUser


@pytest.mark.django_db
class TestLoginView:

    @pytest.fixture
    def username(self):
        return 'mariusz'

    @pytest.fixture
    def password(self):
        return 'admin1'

    @pytest.fixture
    def request_body(self, username, password):
        return json.dumps({'login': username, 'password': password})

    @pytest.fixture
    def login_request(self, request_body, username, password):
        request = APIRequestFactory().post('/api/login', content_type = 'application/json', data = request_body)
        return request

    @pytest.fixture
    def auth_user(self, username, password):
        return User.objects.create_user(username, 'mariusz@test.com', password)

    @pytest.fixture
    def app_user(self, auth_user):
        return AppUser.objects.create(user = auth_user)

    def test_login_unauthorized_status(self, login_request, request_body, username, password):
        response = login(login_request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_ok_status(self, login_request, request_body, username, password, app_user):
        response = login(login_request)
        assert response.status_code == status.HTTP_200_OK

    def test_login_unauthorized_body(self, login_request, request_body, username, password):
        response = login(login_request)
        assert 'message' in json.loads(response.content).keys()

    def test_login_ok_body(self, login_request, request_body, username, password, app_user):
        response = login(login_request)
        assert json.loads(response.content) == {
            'token': username,
            'role': app_user.role.label
        }
