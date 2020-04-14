import os
import click
from flask import Flask

from .settings import config
from .blueprints import auth_bp, blog_bp
from .extension import db, migrate, login_manager, csrf
from .models import User, Post


def create_app():
    config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    os.makedirs(app.instance_path, exist_ok=True)
    config_obj = config[config_name](app.instance_path)
    app.config.from_object(config_obj)

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

    @app.cli.command(help='Generate fake entries in database. '
        'Do *not* use this command in production environment.')
    @click.option('-u', '--user-num', default=20,
        help='Quantity of users. (Default: 20)')
    @click.option('-p', '--post-num', default=100,
        help='Quantity of posts. (Default: 100)')
    def forge(user_num, post_num):
        import random
        from faker import Faker
        fake = Faker()
        db.drop_all()
        db.create_all()

        click.echo('Generating fake entries in database ...')

        for i in range(user_num):
            user = User(name=fake.name())
            user.set_password('fake_password')
            db.session.add(user)
        db.session.commit()

        if user_num > 0:
            for i in range(post_num):
                user = random.choice(User.query.all())
                post = Post(
                    title=fake.sentence(),
                    body=fake.text(),
                    created=fake.date_time_this_year()
                )
                post.author = user
                db.session.add(post)
            db.session.commit()

        click.echo('Done!')
