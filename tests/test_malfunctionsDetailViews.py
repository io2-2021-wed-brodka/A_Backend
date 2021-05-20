import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.enums import BikeState
from BikeRentalApi.models import Bike, Malfunction
from BikeRentalApi.views import malfunctions_detail


@pytest.mark.django_db
class TestMalfunctionsDetailViews:

    @pytest.fixture
    def tech(self):
        tech = User.objects.create(
            username='Mariusz', first_name='Mariusz', last_name='Tester', email='mariusz@test.com',
            password='test123')
        return models.Tech.objects.create(user=tech)

    @pytest.fixture
    def user(self):
        user = User.objects.create(
            username='Janek', first_name='Janek', last_name='Tester', email='Janek@test.com',
            password='test1234')
        return models.AppUser.objects.create(user=user)

    @pytest.fixture
    def admin(self):
        user = User.objects.create(
            username='Pawel', first_name='Pawel', last_name='Tester', email='Pawel@test.com',
            password='test1234')
        return models.Admin.objects.create(user=user)

    @pytest.fixture
    def bike(self, user):
        return Bike.objects.create(station=None, bike_state=BikeState.Working)

    @pytest.fixture
    def malfunction(self, bike, user):
        return Malfunction.objects.create(bike=bike, description="", reporting_user=user.user)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_delete_malfunctions_detail_user_status(self, factory, malfunction, user):
        request = factory.delete(f'/api/malfunctions/{malfunction.pk}')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = malfunctions_detail(request, malfunction.pk)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_malfunctions_detail_tech_status(self, factory, malfunction, tech):
        request = factory.delete(f'/api/malfunctions/{malfunction.pk}')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = malfunctions_detail(request, malfunction.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_malfunctions_detail_admin_status(self, factory, malfunction, admin):
        request = factory.delete(f'/api/malfunctions/{malfunction.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = malfunctions_detail(request, malfunction.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_malfunctions_detail_wrong_request(self, factory, malfunction, admin):
        request = factory.delete(f'/api/malfunctions/{malfunction.pk + 1}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = malfunctions_detail(request, malfunction.pk + 1)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_malfunctions_detail_wrong_request_response_headers(self, factory, malfunction, admin):
        request = factory.delete(f'/api/malfunctions/{malfunction.pk + 1}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = malfunctions_detail(request, malfunction.pk + 1)
        assert set(json.loads(response.content).keys()) == {'message'}
