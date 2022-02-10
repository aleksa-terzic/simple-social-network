
import pytest
from django.db.models.signals import post_save

from users.models import Profile, User


@pytest.mark.unit
def test_user_and_profile_model():
    user = User(id=1, email="aleksa@gmail.com", password="mypass")
    profile = Profile(user=user, city="Belgrade",
                      country="Serbia", holiday="Orthodox Christmas")

    assert user.id == 1
    assert user.email == "aleksa@gmail.com"

    assert profile.user == user
    assert profile.city == "Belgrade"
    assert profile.country == "Serbia"
    assert profile.holiday == "Orthodox Christmas"


@pytest.mark.unit
def test_user_post_save(mocker):
    instance = User(id=1, email="aleksa@gmail.com", password="mypass")
    mock = mocker.patch('users.models.create_profile')

    post_save.send(User, instance=instance, created=True)
    mock.assert_called_with(instance)
