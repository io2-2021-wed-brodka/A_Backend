import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.views import techs_detail


@pytest.mark.django_db
class TestBikesDetailViews:

    @pytest.fixture
    def tech(self):
        tech = User.objects.create(
            username = 'Mariusz', first_name = 'Mariusz', last_name = 'Tester', email = 'mariusz@test.com',
            password = 'test123')
        return models.Tech.objects.create(user = tech)

    @pytest.fixture
    def tech2(self):
        tech = User.objects.create(
            username = 'Ryszard', first_name = 'Ryszard', last_name = 'Andrzejewski', email = 'peja@997.com',
            password = 'DTKJ123')
        return models.Tech.objects.create(user = tech)

    @pytest.fixture
    def user(self):
        user = User.objects.create(
            username = 'Janek', first_name = 'Janek', last_name = 'Tester', email = 'Janek@test.com',
            password = 'test1234')
        return models.AppUser.objects.create(user = user)

    @pytest.fixture
    def admin(self):
        user = User.objects.create(
            username = 'Pawel', first_name = 'Pawel', last_name = 'Tester', email = 'Pawel@test.com',
            password = 'test1234')
        return models.Admin.objects.create(user = user)

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_delete_techs_detail_user_status(self, factory, tech2, user):
        request = factory.delete(f'/api/tech/{tech2.pk}')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = techs_detail(request, tech2.pk)
        assert response.status_code == 401

    def test_delete_techs_detail_tech_status(self, factory, tech2, tech):
        request = factory.delete(f'/api/tech/{tech2.pk}')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = techs_detail(request, tech2.pk)
        assert response.status_code == 401

    def test_delete_techs_detail_admin_status(self, factory, tech2, admin):
        request = factory.delete(f'/api/tech/{tech2.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = techs_detail(request, tech2.pk)
        assert response.status_code == 200

    def test_delete_techs_detail_admin_bad_request(self, factory, admin):
        request = factory.delete(f'/api/bikes/{420}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = techs_detail(request, 420)
        assert response.status_code == 404
        assert 'message' in json.loads(response.content).keys()

    def test_delete_techs_detail_admin_duplicate_request2(self, factory, tech2, admin):
        request = factory.delete(f'/api/tech/{tech2.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = techs_detail(request, tech2.pk)
        assert response.status_code == 200

        response = techs_detail(request, tech2.pk)
        assert response.status_code == 404
        assert 'message' in json.loads(response.content).keys()

    def test_delete_bikes_detail_admin_response(self, factory, tech2, admin):
        request = factory.delete(f'/api/bikes/{tech2.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        tech_id = tech2.pk
        tech_name = tech2.user.username

        response = techs_detail(request, tech2.pk)

        assert json.loads(response.content) == {
            'id': tech_id,
            'name': tech_name
        }

    def test_get_techs_detail_user_status(self, factory, tech2, user):
        request = factory.get(f'/api/tech/{tech2.pk}')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = techs_detail(request, tech2.pk)
        assert response.status_code == 401

    def test_get_techs_detail_tech_status(self, factory, tech2, tech):
        request = factory.get(f'/api/tech/{tech2.pk}')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = techs_detail(request, tech2.pk)
        assert response.status_code == 401

    def test_get_techs_detail_admin_status(self, factory, tech2, admin):
        request = factory.get(f'/api/tech/{tech2.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = techs_detail(request, tech2.pk)
        assert response.status_code == 200

    def test_get_techs_detail_admin_bad_request(self, factory, admin):
        request = factory.get(f'/api/bikes/{420}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = techs_detail(request, 420)
        assert response.status_code == 404
        assert 'message' in json.loads(response.content).keys()

    def test_get_bikes_detail_admin_response(self, factory, tech2, admin):
        request = factory.get(f'/api/bikes/{tech2.pk}')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        tech_id = tech2.pk
        tech_name = tech2.user.username

        response = techs_detail(request, tech2.pk)

        assert json.loads(response.content) == {
            'id': tech_id,
            'name': tech_name
        }
