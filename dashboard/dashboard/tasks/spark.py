from . import celery


@celery.task
def run_spark():
    pass
