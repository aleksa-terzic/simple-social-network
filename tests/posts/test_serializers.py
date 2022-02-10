import pytest

from posts.api.serializers import PostSerializer
from posts.models import Post
from users.models import User


class TestPostSerializer:

    @pytest.mark.django_db
    def test_serialize_model(self):
        user = User.objects.create_user("aleksa@gmail.com", "mypass")
        post = Post.objects.create(author=user, title="Title", body="body")
        serializer = PostSerializer(post)

        assert serializer.data

    @pytest.mark.django_db
    def test_serialized_data(self):
        valid_serialized_data = {
            "author": 1,
            "title": "Title",
            "body": "Body"
        }
        serializer = PostSerializer(data=valid_serialized_data)

        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}
