import pytest
from model_bakery import baker


@pytest.fixture
def pbb(db):
    def post_bakery_batch(n):
        pbb = baker.make('posts.Post', _fill_optional=['title', 'body', 'users_like'], _quantity=n)
        return pbb
    return post_bakery_batch

@pytest.fixture
def pb(db):
    def post_bakery():
        pb = baker.make('posts.Post', _fill_optional=['title', 'body', 'users_like'])
        return pb
    return post_bakery