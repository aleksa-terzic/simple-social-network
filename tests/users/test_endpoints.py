from urllib import response
import json

import pytest
from django.urls import reverse

from users.models import User

pytestmark = pytest.mark.django_db


class TestUserEndpoints:

    def test_signup(self, api_client):
        data = {
            "email": 'aleksa@gmail.com',
            "password": "mypass"
        }
        url = reverse('signup')
        response = api_client.post(url, data=data, format='json')
        body = json.loads(response.content)

        assert response.status_code == 201
        assert body['id'] is not None
        assert body['email'] == data['email']

    def test_login(self, api_client):
        # create user
        user = User.objects.create_user('aleksa@gmail.com', 'mypass')
        url = reverse('login')
        login_data = {
            "email": user.email,
            "password": "mypass"
        }
        # get token through login
        response = api_client.post(url, data=login_data, format='json')
        assert response.status_code == 200
        assert response.data['access'] is not None
        assert response.data['refresh'] is not None

    def test_get_user_data(self, api_client):
        # create user
        user = User.objects.create_user('aleksa@gmail.com', 'mypass')
        url = reverse('login')
        login_data = {
            "email": user.email,
            "password": "mypass"
        }
        print(user.id)
        # get token
        token = api_client.post(url, data=login_data, format='json')
        assert token.data['access'] is not None

        api_client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token.data['access'])

        user_data_url = reverse('get_user_data', kwargs={'pk': user.id})
        response = api_client.get(user_data_url, format='json')

        assert response.status_code == 200
