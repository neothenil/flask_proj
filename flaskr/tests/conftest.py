import os
import tempfile
from pathlib import Path

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db


_file = Path(Path(__file__).parent, 'data.sql')
with _file.open() as f:
    _data_sql = f.read()


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:

    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        resp = self._client.post('/auth/login',
            data={'username': username, 'password': password})
        return resp

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
