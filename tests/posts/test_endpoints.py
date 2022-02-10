import json

import pytest
from django.urls import reverse
from users.models import User

from posts.models import Post


class TestPostEndpoints:

    def test_list(self, api_client, pbb):
        pbb(3)
        url = reverse('posts_list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, auth_api_client, pbb, user_1):
        post = pbb(1)[0]
        valid_data = {
            'author': user_1.id,
            'title': post.title,
            'body': post.body
        }

        url = reverse('posts_list')
        response = auth_api_client.post(url, valid_data, format='json')

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

    def test_update_not_authorized(self, auth_api_client, pb, user_1):
        post = pb()
        updated_data = {
            "title": "New title",
            "body": "New body"
        }

        url = reverse('post_detail', kwargs={'pk': post.id})
        response = auth_api_client.put(url, updated_data, format='json')

        assert response.status_code == 401
        assert user_1.id != post.author.id

    def test_update(self, auth_api_client, user_1):
        post = Post.objects.create(
            author=user_1, title="Old title", body="Old post body")

        updated_data = {
            "title": "New title",
            "body": "New body"
        }

        url = reverse('post_detail', kwargs={'pk': post.id})
        response = auth_api_client.put(url, updated_data, format='json')

        assert response.status_code == 200
        assert user_1.id == post.author.id

    def test_delete(self, auth_api_client, user_1):
        post = Post.objects.create(
            author=user_1, title="Old title", body="Old post body")
        url = reverse('post_detail', kwargs={'pk': post.id})

        response = auth_api_client.delete(url, format='json')

        assert response.status_code == 204
