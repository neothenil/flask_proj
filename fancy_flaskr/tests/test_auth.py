import pytest

from flaskr import create_app
from flaskr.extension import db
from flaskr.models import User, Post

from .conftest import fakes, AuthActions


@pytest.mark.parametrize('data', fakes['users'])
def test_register(client, data):
    assert client.get('/auth/register').status_code == 200
    with client:
        response = client.post('/auth/register',
                data={'username': data['username'],
                      'password': data['password']})
        assert response.status_code == 302
        assert '/auth/login' in response.headers['Location']
        user = User.query.filter_by(name=data['username']).first()
        assert user is not None


@pytest.fixture
def registered_user(client):
    user = fakes['users'][0]
    client.post('/auth/register', data=user)
    return user


def test_login(client, registered_user):
    assert client.get('/auth/login').status_code == 200
    response = client.post('/auth/login', data=registered_user)
    assert response.status_code == 302
    assert '/post' in response.headers['Location']
    assert client.get('/auth/login').status_code == 302
    client.get('/auth/logout')
    response = client.post('/auth/login', data=registered_user,
            follow_redirects=True)
    assert 'You have logged in' in response.get_data(as_text=True)


def test_logout(client, registered_user, auth):
    assert client.get('/auth/logout').status_code == 302
    auth.login(registered_user['username'],
               registered_user['password'])
    response = client.get('/auth/logout', follow_redirects=True)
    assert 'You have logged out' in response.get_data(as_text=True)


def test_before_login(auth_app):
    client = auth_app.test_client()
    data = (
        ('/', 200), ('/post/', 200),
        ('/post/create', 302), ('/post/1/update', 302)
    )
    for url, status in data:
        assert client.get(url).status_code == status


def test_after_login(auth_app):
    client = auth_app.test_client()
    auth = AuthActions(client)
    res = auth.login(fakes['users'][0]['username'],
            fakes['users'][0]['password'])
    assert res.status_code == 302
    data = (
        ('/', 200), ('/post/', 200),
        ('/post/create', 200), ('/post/1/update', 200)
    )
    for url, status in data:
        assert client.get(url).status_code == status


def test_update_post(auth_app):
    client = auth_app.test_client()
    auth = AuthActions(client)
    res = auth.login(fakes['users'][0]['username'],
            fakes['users'][0]['password'])
    assert res.status_code == 302
    with auth_app.app_context():
        posts = Post.query.all()
        author_names = [post.author.name for post in posts]
    for post, author_name in zip(posts, author_names):
        url = '/post/%d/update' % post.id
        res = client.get(url)
        if author_name == fakes['users'][0]['username']:
            assert res.status_code == 200
        else:
            assert res.status_code == 404
