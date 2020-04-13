import os
import click
from flask import Flask

from .settings import config
from .blueprints import auth_bp, blog_bp
from .extension import db, migrate, login_manager, csrf


def create_app():
    config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)


def register_commands(app):
    @app.cli.command('create-db', help='Create database.')
    @click.option('-f', '--force',
        is_flag=True, help='Drop old database if it exists.')
    def create_db(force):
        if force:
            db.drop_all()
        db.create_all()
        click.echo('database created.')
