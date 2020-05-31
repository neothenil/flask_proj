import os
from random import randint
from flask import Flask, render_template

from .settings import config
from .blueprints import auth_bp, task_bp
from .utils import fake_tasks


def create_app():
    config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    os.makedirs(app.instance_path, exist_ok=True)
    config_obj = config[config_name](app.instance_path)
    app.config.from_object(config_obj)

    register_extensions(app)
    register_blueprints(app)
    register_routes(app)
    register_commands(app)

    return app


def register_extensions(app):
    pass


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)


def register_routes(app):
    @app.route('/', methods=['GET'])
    def index():
        locust_tasks = fake_tasks(randint(0, 10))
        spark_tasks = fake_tasks(randint(0, 10))
        return render_template('index.html', locust_tasks=locust_tasks,
                spark_tasks=spark_tasks)


def register_commands(app):
    pass
