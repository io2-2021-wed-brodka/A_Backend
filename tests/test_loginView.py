import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi.auth_views import login


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

    def test_login_unauthorized_status(self, login_request, request_body, username, password):
        response = login(login_request)
        assert response.status_code == 401

    def test_login_ok_status(self, login_request, request_body, username, password, auth_user):
        response = login(login_request)
        assert response.status_code == 200

    def test_login_unauthorized_body(self, login_request, request_body, username, password):
        response = login(login_request)
        assert 'message' in json.loads(response.content).keys()

    def test_login_ok_body(self, login_request, request_body, username, password, auth_user):
        response = login(login_request)
        assert json.loads(response.content) == {'token': username}
