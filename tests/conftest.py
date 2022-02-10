import pytest
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def user_1(db):
    user = User.objects.create_user(email="aleksa@gmail.com", password="mypass")
    return user

@pytest.fixture
def auth_api_client(db, user_1, api_client):
    refresh = RefreshToken.for_user(user_1)
    api_client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))

    return api_client