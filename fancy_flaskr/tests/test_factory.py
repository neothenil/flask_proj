import pytest

from flaskr import create_app
from flaskr.settings import config


@pytest.mark.parametrize(('config_name', 'extra'), (
    ('development', {'ENV': 'development', 'DEBUG': True, 'TESTING': False}),
    ('testing', {'ENV': 'testing', 'DEBUG': False, 'TESTING': True}),
    ('production', {'ENV': 'production', 'DEBUG': False, 'TESTING': False})))
def test_config(monkeypatch, config_name, extra):
    monkeypatch.setenv('FLASK_ENV', config_name)
    app = create_app()
    config_obj = config[config_name]
    for attr in dir(config_obj):
        if not attr.startswith('_') and attr.isupper():
            assert app.config[attr] == getattr(config_obj, attr)
    for attr, value in extra.items():
        assert app.config[attr] == value


@pytest.mark.parametrize('config_name',
    ('wrong', 'bad', 'false', 'wtf'))
def test_wrong_config(monkeypatch, config_name):
    monkeypatch.setenv('FLASK_ENV', config_name)
    with pytest.raises(KeyError):
        create_app()
