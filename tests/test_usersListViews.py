import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.views import users_list


@pytest.mark.django_db
class TestUsersListViews:

    @pytest.fixture
    def user(self):
        user = User.objects.create(
            username = 'Janek', first_name = 'Janek', last_name = 'Tester', email = 'Janek@test.com',
            password = 'test1234')
        return models.AppUser.objects.create(user = user)

    @pytest.fixture
    def tech(self):
        tech = User.objects.create(
            username = 'Mariusz', first_name = 'Mariusz', last_name = 'Tester', email = 'mariusz@test.com',
            password = 'test123')
        return models.Tech.objects.create(user = tech)

    @pytest.fixture
    def admin(self):
        user = User.objects.create(
            username = 'Pawel', first_name = 'Pawel', last_name = 'Tester', email = 'Pawel@test.com',
            password = 'test1234')
        return models.Admin.objects.create(user = user)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_get_users_list_user_status(self, factory, user):
        request = factory.get('/api/users')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = users_list(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_techs_list_tech_status(self, factory, tech):
        request = factory.get('/api/users')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = users_list(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_techs_list_admin_status(self, factory, admin):
        request = factory.get('/api/users')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = users_list(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_techs_list_admin_body(self, factory, user, tech, admin):
        request = factory.get('/api/users')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = users_list(request)

        assert json.loads(response.content) == {
            "users": [
                {
                    'id': str(user.pk),
                    'name': user.user.username
                }
            ]
        }
