import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from BikeRentalApi import models
from BikeRentalApi.views import techs_list


@pytest.mark.django_db
class TestBikesListViews:

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

    def test_get_techs_list_user_status(self, factory, user):
        request = factory.get('/api/techs')
        request.headers = {'Authorization': f'Bearer {user.user.username}'}

        response = techs_list(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_techs_list_tech_status(self, factory, tech):
        request = factory.get('/api/techs')
        request.headers = {'Authorization': f'Bearer {tech.user.username}'}

        response = techs_list(request)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_techs_list_admin_status(self, factory, admin):
        request = factory.get('/api/techs')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = techs_list(request)

        assert response.status_code == status.HTTP_200_OK

    def test_get_techs_list_admin_body(self, factory, user, tech, admin):
        request = factory.get('api/bikes')
        request.headers = {'Authorization': f'Bearer {admin.user.username}'}

        response = techs_list(request)

        assert json.loads(response.content) == [
            {
                'id': str(tech.pk),
                'name': tech.user.username
            }
        ]

    def test_post_techs_list_user_status(self, factory, user):
        body = json.dumps({'name': 'NowyMariusz', 'password': '123456'})
        request = factory.post('/api/techs', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {user.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = techs_list(request)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_techs_list_tech_status(self, factory, tech):
        body = json.dumps({'name': 'NowyMariusz', 'password': '123456'})
        request = factory.post('/api/techs', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {tech.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = techs_list(request)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_techs_list_admin_status(self, factory, admin):
        body = json.dumps({'name': 'NowyMariusz', 'password': '123456'})
        request = factory.post('/api/techs', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = techs_list(request)

        assert response.status_code == status.HTTP_200_OK

    def test_post_tech_list_admin_response(self, factory, admin):
        body = json.dumps({'name': 'NowyMariusz', 'password': '123456'})
        request = factory.post('/api/techs', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = techs_list(request)
        data = json.loads(response.content)

        assert isinstance(data['id'], str) \
               and data['name'] == 'NowyMariusz' \
               and set(data.keys()) == {'id', 'name'}

    def test_post_tech_list_duplicate_request_status(self, factory, admin):
        body = json.dumps({'name': 'NowyMariusz', 'password': '123456'})
        request = factory.post('/api/techs', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = techs_list(request)
        assert response.status_code == status.HTTP_200_OK

        response = techs_list(request)
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_post_tech_list_bad_request_status(self, factory, admin):
        body = json.dumps({'namee': 'NowyMariusz', 'password': '123456'})
        request = factory.post('/api/techs', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = techs_list(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_tech_list_bad_request2_status(self, factory, admin):
        body = json.dumps({'name': 'NowyMariusz'})
        request = factory.post('/api/techs', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = techs_list(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_tech_list_bad_request3_status(self, factory, admin):
        body = json.dumps({'password': '421412'})
        request = factory.post('/api/techs', content_type = 'application/json', data = body)
        headers = {'Authorization': f'Bearer {admin.user.username}'}
        headers.update(request.headers)
        request.headers = headers

        response = techs_list(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
