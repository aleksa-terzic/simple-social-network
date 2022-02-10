import pytest

from users.api.serializers import UserSerializer
from users.models import User


class TestUserSerializer:

    @pytest.mark.django_db
    def test_serialize_model(self):
        user = User.objects.create_user('aleksa@gmail.com', 'mypass')
        serializer = UserSerializer(user)

        assert serializer.data

    @pytest.mark.django_db
    def test_serialized_data(self):
        valid_serialized_data = {
            "email": "aleksa@gmail.com",
            "password": "mypass"
        }
        serializer = UserSerializer(data=valid_serialized_data)

        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}
