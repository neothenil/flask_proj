import os
from celery import Celery

from ..settings import config


def create_celery():
    config_name = os.getenv("FLASK_ENV", "development")
    config_obj = config[config_name](".")
    celery = Celery(
        __name__,
        backend=config_obj.CELERY_RESULT_BACKEND,
        broker=config_obj.CELERY_BROKER_URL,
    )
    celery.config_from_object(config_obj)
    return celery


celery = create_celery()

from .locust import run_locust
from .spark import run_spark
from .demo import add