import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import UserState
from BikeRentalApi.views import users_blocked_list


@pytest.mark.django_db
class TestUsersBlockedListViews:

    @pytest.fixture
    def tech(self):
        tech = User.objects.create(
            username = 'Mariusz', first_name = 'Mariusz', last_name = 'Tester', email = 'mariusz@test.com',
            password = 'test123')
        return models.Tech.objects.create(user = tech)

    @pytest.fixture
    def blocked_user(self):
        user = User.objects.create(
            username = 'Janek', first_name = 'Janek', last_name = 'Tester', email = 'Janek@test.com',
            password = 'test1234')
        return models.AppUser.objects.create(user = user, state = UserState.Banned)

    @pytest.fixture
    def working_user(self):
        user = User.objects.create(
            username = 'Bartosz', first_name = 'Bartosz', last_name = 'Tester', email = 'Bartosz@test.com',
            password = 'test1234')
        return models.AppUser.objects.create(user = user, state = UserState.Active)

    @pytest.fixture
    def admin(self):
        user = User.objects.create(
            username = 'Pawel', first_name = 'Pawel', last_name = 'Tester', email = 'Pawel@test.com',
            password = 'test1234')
        return models.Admin.objects.create(user = user)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_get_users_blocked_list_user_response_code(self, factory, working_user):
        request = factory.get('/api/users/blocked')
        request.headers = {'Authorization': f'Bearer {working_user.user.username}'}

        response = users_blocked_list(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_users_blocked_list_tech_response_code(self, factory, tech):
        request = factory.get('/api/users/blocked')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = users_blocked_list(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_users_blocked_list_admin_response_code(self, factory, admin):
        request = factory.get('/api/users/blocked')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = users_blocked_list(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_users_blocked_list_admin_response_body(self, factory, admin, blocked_user):
        request = factory.get('/api/users/blocked')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = users_blocked_list(request)
        assert json.loads(response.content) == {
            'users': [
                {
                    'id': str(blocked_user.pk),
                    'name': blocked_user.user.username
                }
            ]
        }

    def test_post_users_blocked_list_user_status(self, factory, working_user):
        data = json.dumps({'id': str(working_user.pk)})
        request = factory.post(f'/api/users/blocked/', content_type = 'application/json', data = data)
        request.headers = {'Authorization': f'Bearer {working_user.user.username}'}

        response = users_blocked_list(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_users_blocked_list_tech_status(self, factory, tech, working_user):
        data = json.dumps({'id': str(working_user.pk)})
        request = factory.post(f'/api/users/blocked/', content_type = 'application/json', data = data)
        request.headers = {'Authorization': f'Bearer {working_user.user.username}'}

        response = users_blocked_list(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_users_blocked_list_admin_status(self, factory, admin, working_user):
        data = json.dumps({'id': str(working_user.pk)})
        request = factory.post(f'/api/users/blocked/', content_type = 'application/json', data = data)
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = users_blocked_list(request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_users_blocked_list_admin_bad_request(self, factory, admin):
        data = json.dumps({'id': "1337"})
        request = factory.post(f'/api/users/blocked/', content_type = 'application/json', data = data)
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = users_blocked_list(request)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'message' in json.loads(response.content).keys()

    def test_post_users_blocked_list_already_banned_admin(self, factory, admin, blocked_user):
        data = json.dumps({'id': str(blocked_user.pk)})
        request = factory.post(f'/api/users/blocked/', content_type = 'application/json', data = data)
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = users_blocked_list(request)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert 'message' in json.loads(response.content).keys()

    def test_post_users_blocked_list_response(self, factory, admin, working_user):
        data = json.dumps({'id': str(working_user.pk)})
        request = factory.post(f'/api/users/blocked/', content_type = 'application/json', data = data)
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = users_blocked_list(request)
        assert json.loads(response.content) == {
            'id': str(working_user.pk),
            'name': working_user.user.username
        }
