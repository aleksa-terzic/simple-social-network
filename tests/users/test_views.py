from rest_framework.test import APIRequestFactory, force_authenticate
from users.models import User, Profile
from users.api.views import GetUserData
from django.urls import reverse
import pytest

factory = APIRequestFactory()

pytestmark = pytest.mark.django_db

class TestUserViews:

    def test_user_data(self):
        user = User.objects.create_user('aleksa@gmail.com', 'mypass')

        url = reverse('get_user_data', kwargs={'pk': user.id})

        view = GetUserData.as_view()

        request = factory.get(url)
        force_authenticate(request, user=user)

        response = view(request, pk=user.id).render()

        assert response.status_code == 200
        assert response.data['profile']['user'] == user.id