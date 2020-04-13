import pytest

from flaskr import create_app
from flaskr.extension import db


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('FLASK_ENV', 'testing')
    app = create_app()
    db.create_all()
    return app
