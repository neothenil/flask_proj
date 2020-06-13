import os
import click
from random import randint
from pathlib import Path
from flask import Flask, render_template, request, abort, send_from_directory
from flask_login import login_required, current_user

from .settings import config
from .blueprints import auth_bp, task_bp
from .blueprints.task import update_tasks
from .extension import db, migrate, login_manager, csrf
from .models import Task


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
        locust_tasks = (
            Task.query.filter_by(user_id=current_user.id, type="LOCUST")
            .order_by(Task.timestamp.desc())
            .all()
        )
        spark_tasks = (
            Task.query.filter_by(user_id=current_user.id, type="SPARK")
            .order_by(Task.timestamp.desc())
            .all()
        )
        update_tasks(locust_tasks)
        update_tasks(spark_tasks)
        return render_template(
            "index.html", locust_tasks=locust_tasks, spark_tasks=spark_tasks
        )

    @app.route("/help", methods=["GET"])
    def help():
        locust_demo_dir = Path(app.static_folder, "demo", "locust")
        spark_demo_dir = Path(app.static_folder, "demo", "spark")
        locust_zipfiles = filter(
            lambda x: x.endswith(".zip"), os.listdir(locust_demo_dir)
        )
        spark_zipfiles = filter(
            lambda x: x.endswith(".zip"), os.listdir(spark_demo_dir)
        )
        locust_zipfiles = list(
            map(lambda x: os.path.splitext(x)[0], locust_zipfiles)
        )
        spark_zipfiles = list(
            map(lambda x: os.path.splitext(x)[0], spark_zipfiles)
        )
        return render_template(
            "help.html",
            locust_zipfiles=locust_zipfiles,
            spark_zipfiles=spark_zipfiles,
        )

    @app.route("/help/demo", methods=["GET"])
    def demo():
        type = request.args.get("type")
        if type is None:
            abort(404)
        filename = request.args.get("filename")
        if filename is None:
            abort(404)
        demo_dir = Path(app.static_folder, "demo", type)
        demo = Path(demo_dir, filename)
        if not demo.exists():
            abort(404)
        return send_from_directory(
            demo_dir, filename, as_attachment=True, attachment_filename=filename
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
