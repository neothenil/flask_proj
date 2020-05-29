import os
import click
from flask import Flask

from .settings import config
from .extension import db, migrate, login_manager, csrf


def create_app():
    config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    os.makedirs(app.instance_path, exist_ok=True)
    config_obj = config[config_name](app.instance_path)
    app.config.from_object(config_obj)

    register_extensions(app)
    register_blueprints(app)
    register_rules(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    pass


def register_rules(app):
    pass


def register_commands(app):
    pass
