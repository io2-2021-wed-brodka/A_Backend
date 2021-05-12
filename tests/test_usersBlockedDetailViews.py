import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import StationState, UserState
from BikeRentalApi.models import BikeStation
from BikeRentalApi.views import users_blocked_detail


@pytest.mark.django_db
class TestUsersBlockedDetailViews:

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

    def test_get_users_blocked_detail_user_response_code(self, factory, working_user, blocked_user):
        request = factory.delete(f'/api/users/blocked/{blocked_user.pk}')
        request.headers = {'Authorization': f'Bearer {working_user.user.username}'}

        response = users_blocked_detail(request, blocked_user.pk)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_users_blocked_detail_tech_response_code(self, factory, tech, blocked_user):
        request = factory.delete(f'/api/users/blocked/{blocked_user.pk}')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = users_blocked_detail(request, blocked_user.pk)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_users_blocked_detail_admin_response_code(self, factory, admin, blocked_user):
        request = factory.delete(f'/api/users/blocked/{blocked_user.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = users_blocked_detail(request, blocked_user.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_get_users_blocked_detail_admin_bad_user(self, factory, admin):
        request = factory.delete(f'/api/users/blocked/1457')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = users_blocked_detail(request, 1457)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_users_blocked_detail_admin_unblocked_user(self, factory, admin, working_user):
        request = factory.delete(f'/api/users/blocked/{working_user.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = users_blocked_detail(request, working_user.pk)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
