import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi.auth_views import register


@pytest.mark.django_db
class TestRegisterView:

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
    def register_request(self, request_body, username, password):
        request = APIRequestFactory().post('/api/register', content_type = 'application/json', data = request_body)
        return request

    @pytest.fixture
    def login_request(self, request_body, username, password):
        request = APIRequestFactory().post('/api/login', content_type = 'application/json', data = request_body)
        return request

    @pytest.fixture
    def auth_user(self, username, password):
        return User.objects.create_user(username, 'mariusz@test.com', password)

    def test_register_conflict_status(self, register_request, request_body, username, password, auth_user):
        response = register(register_request)
        assert response.status_code == 409

    def test_register_ok_status(self, register_request, request_body, username, password):
        response = register(register_request)
        assert response.status_code == 200

    def test_register_conflict_body(self, register_request, request_body, username, password, auth_user):
        response = register(register_request)
        assert 'message' in json.loads(response.content).keys()

    def test_register_ok_body(self, register_request, request_body, username, password):
        response = register(register_request)
        assert json.loads(response.content) == {'token': username}
