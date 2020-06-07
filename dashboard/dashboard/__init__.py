import os
import click
from random import randint
from flask import Flask, render_template
from flask_login import login_required, current_user

from .settings import config
from .utils import fake_tasks
from .blueprints import auth_bp, task_bp
from .blueprints.task import update_tasks
from .extension import db, migrate, login_manager, csrf


def create_app():
    config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    config_obj = config[config_name](app.instance_path)
    app.config.from_object(config_obj)

    register_extensions(app)
    register_blueprints(app)
    register_routes(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)


def register_routes(app):
    @app.route("/", methods=["GET"])
    @login_required
    def index():
        user = current_user._get_current_object()
        tasks = user.tasks
        locust_tasks = list(filter(lambda x: x.type == "LOCUST", tasks))
        spark_tasks = list(filter(lambda x: x.type == "SPARK", tasks))
        update_tasks(locust_tasks)
        update_tasks(spark_tasks)
        return render_template(
            "index.html", locust_tasks=locust_tasks, spark_tasks=spark_tasks
        )


def register_commands(app):
    @app.cli.command("create-db", help="Create database.")
    @click.option(
        "-f", "--force", is_flag=True, help="Drop old database if it exists."
    )
    def create_db(force):
        if force:
            db.drop_all()
            click.echo("old database dropped.")
        db.create_all()
        click.echo("database created.")
