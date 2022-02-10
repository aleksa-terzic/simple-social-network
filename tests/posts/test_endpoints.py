import json

import pytest
from django.urls import reverse
from users.models import User

from posts.models import Post

pytestmark = pytest.mark.django_db


class TestPostEndpoints:

    def test_list(self, api_client, pbb):
        pbb(3)
        url = reverse('posts_list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client, pbb):
        user = User.objects.create_user('aleksa@gmail.com', 'mypass')
        login_url = reverse('login')
        login_data = {
            "email": user.email,
            "password": "mypass"
        }
        token = api_client.post(login_url, data=login_data, format='json')
        assert token.data['access'] is not None

        api_client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token.data['access'])

        post = pbb(1)[0]
        valid_data = {
            'author': user.id,
            'title': post.title,
            'body': post.body
        }
        url = reverse('posts_list')

        response = api_client.post(url, valid_data, format='json')

        assert response.status_code == 201

    def test_retrieve(self, api_client, pb):
        post = pb()
        post = Post.objects.last()
        expected_data = post.__dict__
        expected_data['author'] = post.author.id
        expected_data['title'] = post.title
        expected_data['body'] = post.body
        expected_data['likes'] = post.users_like.count()
        expected_data['created_at'] = post.created_at.strftime(
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )

        expected_data.pop('_state')
        expected_data.pop('author_id')

        url = reverse('post_detail', kwargs={'pk': post.id})

        response = api_client.get(url)
        data = json.loads(response.content)

        assert response.status_code == 200
        assert data == expected_data

    def test_update_not_authorized(self, api_client, pb):
        user = User.objects.create_user('aleksa@gmail.com', 'mypass')
        login_url = reverse('login')
        login_data = {
            "email": user.email,
            "password": "mypass"
        }
        token = api_client.post(login_url, data=login_data, format='json')
        assert token.data['access'] is not None

        api_client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token.data['access'])

        post = pb()
        updated_data = {
            "title": "New title",
            "body": "New body"
        }

        url = reverse('post_detail', kwargs={'pk': post.id})
        response = api_client.put(url, updated_data, format='json')

        assert response.status_code == 401
        assert user.id != post.author.id

    def test_update(self, api_client):
        user = User.objects.create_user('aleksa@gmail.com', 'mypass')
        post = Post.objects.create(
            author=user, title="Old title", body="Old post body")

        login_url = reverse('login')
        login_data = {
            "email": user.email,
            "password": "mypass"
        }
        token = api_client.post(login_url, data=login_data, format='json')
        assert token.data['access'] is not None

        api_client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token.data['access'])

        updated_data = {
            "title": "New title",
            "body": "New body"
        }

        url = reverse('post_detail', kwargs={'pk': post.id})

        response = api_client.put(url, updated_data, format='json')

        assert response.status_code == 200
        assert user.id == post.author.id

    def test_delete(self, api_client):
        user = User.objects.create_user('aleksa@gmail.com', 'mypass')
        post = Post.objects.create(
            author=user, title="Old title", body="Old post body")

        login_url = reverse('login')
        login_data = {
            "email": user.email,
            "password": "mypass"
        }
        token = api_client.post(login_url, data=login_data, format='json')
        assert token.data['access'] is not None

        api_client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token.data['access'])

        url = reverse('post_detail', kwargs={'pk': post.id})

        response = api_client.delete(url, format='json')

        assert response.status_code == 204
