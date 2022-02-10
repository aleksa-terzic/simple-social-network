import pytest
from users.models import User

from posts.models import Like, Post


@pytest.mark.unit
def test_post_model():
    user = User(id=1)
    post = Post(id=1, author=user, title="Post title", body="Post body")

    assert post.id == 1
    assert post.author.id == 1
    assert post.title == "Post title"
    assert post.body == "Post body"


@pytest.mark.unit
def test_like_model():
    user = User(id=1)
    post = Post(id=1, author=user)
    like = Like(post=post, user=user)

    assert like.user.id == 1
    assert like.post.id == 1
