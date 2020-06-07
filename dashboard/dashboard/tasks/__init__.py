import os
import dotenv
from pathlib import Path
from celery import Celery

from ..settings import config


def create_celery():
    dotenv.load_dotenv(dotenv_path=".flaskenv")
    config_name = os.getenv("FLASK_ENV", "development")
    root_path = Path(__file__).parent.parent
    config_obj = config[config_name](Path(root_path.parent, "instance"))
    celery = Celery(
        __name__,
        backend=config_obj.CELERY_RESULT_BACKEND,
        broker=config_obj.CELERY_BROKER_URL,
    )
    celery.config_from_object(config_obj)
    celery.conf.update(
        LOCUST_BIN=Path(root_path, "bin", "LOCUST"),
        SPARK_BIN=Path(root_path, "bin", "SPARK"),
    )
    return celery


celery = create_celery()

from .locust import run_locust
from .spark import run_spark
from .demo import add
