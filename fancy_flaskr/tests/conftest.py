import os
import pytest

from flaskr import create_app
from flaskr.extension import db


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('FLASK_ENV', 'testing')
    app = create_app()
    with app.app_context():
        db.create_all()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username, password):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)


fakes = {'users': [
    {'username': 'testing',
     'password': 'testing',
     'posts': [
         {'title': 'post from testing',
          'body': 'testing'},
     ]},
    {'username': 'admin',
     'password': '123456',
     'posts': [
         {'title': 'post from admin',
          'body': 'testing'},
     ]}
    ]}


@pytest.fixture(scope='session')
def auth_app():
    import os
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    with app.app_context():
        db.create_all()
    client = app.test_client()
    for user in fakes['users']:
        client.post('/auth/register',
                    data={'username': user['username'],
                          'password': user['password']})
        client.post('/auth/login',
                    data={'username': user['username'],
                          'password': user['password']})
        for post in user['posts']:
            client.post('/post/create',
                        data={'title': post['title'],
                              'body': post['body']})
        client.get('auth/logout')
    yield app
    os.unsetenv('FLASK_ENV')
