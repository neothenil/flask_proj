import os
from datetime import timedelta
from pathlib import Path


class BaseConfig:

    # Set 'SECRET_KEY' to a random string in env in production.
    SECRET_KEY = os.getenv("SECRET_KEY", "secret string")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(15)
    CELERY_RESULT_BACKEND = os.getenv(
        "CELERY_RESULT_BACKEND", "redis://localhost"
    )
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://localhost")
    POLL_INTERVAL = 0.01

    def __init__(self, basedir):
        pass


class DevelopmentConfig(BaseConfig):
    def __init__(self, basedir):
        locust_dir = Path(basedir, "var", "locust")
        locust_upload_dir = Path(locust_dir, "upload")
        locust_run_dir = Path(locust_dir, "run")
        locust_download_dir = Path(locust_dir, "download")
        spark_dir = Path(basedir, "var", "spark")
        spark_upload_dir = Path(spark_dir, "upload")
        spark_run_dir = Path(spark_dir, "run")
        spark_download_dir = Path(spark_dir, "download")
        os.makedirs(basedir, exist_ok=True)
        os.makedirs(locust_upload_dir, exist_ok=True)
        os.makedirs(locust_run_dir, exist_ok=True)
        os.makedirs(locust_download_dir, exist_ok=True)
        os.makedirs(spark_upload_dir, exist_ok=True)
        os.makedirs(spark_run_dir, exist_ok=True)
        os.makedirs(spark_download_dir, exist_ok=True)
        # Exposed configuration
        self.SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(
            Path(basedir, "database-dev.db").absolute()
        )
        self.LOCUST_UPLOAD_DIR = locust_upload_dir
        self.LOCUST_RUN_DIR = locust_run_dir
        self.LOCUST_DOWNLOAD_DIR = locust_download_dir
        self.SPARK_UPLOAD_DIR = spark_upload_dir
        self.SPARK_RUN_DIR = spark_run_dir
        self.SPARK_DOWNLOAD_DIR = spark_download_dir


class TestingConfig(BaseConfig):

    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    def __init__(self, basedir):
        locust_dir = Path(basedir, "var", "locust")
        locust_upload_dir = Path(locust_dir, "upload")
        locust_run_dir = Path(locust_dir, "run")
        locust_download_dir = Path(locust_dir, "download")
        spark_dir = Path(basedir, "var", "spark")
        spark_upload_dir = Path(spark_dir, "upload")
        spark_run_dir = Path(spark_dir, "run")
        spark_download_dir = Path(spark_dir, "download")
        os.makedirs(basedir, exist_ok=True)
        os.makedirs(locust_upload_dir, exist_ok=True)
        os.makedirs(locust_run_dir, exist_ok=True)
        os.makedirs(locust_download_dir, exist_ok=True)
        os.makedirs(spark_upload_dir, exist_ok=True)
        os.makedirs(spark_run_dir, exist_ok=True)
        os.makedirs(spark_download_dir, exist_ok=True)
        self.LOCUST_UPLOAD_DIR = locust_upload_dir
        self.LOCUST_RUN_DIR = locust_run_dir
        self.LOCUST_DOWNLOAD_DIR = locust_download_dir
        self.SPARK_UPLOAD_DIR = spark_upload_dir
        self.SPARK_RUN_DIR = spark_run_dir
        self.SPARK_DOWNLOAD_DIR = spark_download_dir


class ProductionConfig(BaseConfig):
    def __init__(self, basedir):
        locust_dir = Path(basedir, "var", "locust")
        locust_upload_dir = Path(locust_dir, "upload")
        locust_run_dir = Path(locust_dir, "run")
        locust_download_dir = Path(locust_dir, "download")
        spark_dir = Path(basedir, "var", "spark")
        spark_upload_dir = Path(spark_dir, "upload")
        spark_run_dir = Path(spark_dir, "run")
        spark_download_dir = Path(spark_dir, "download")
        os.makedirs(basedir, exist_ok=True)
        os.makedirs(locust_upload_dir, exist_ok=True)
        os.makedirs(locust_run_dir, exist_ok=True)
        os.makedirs(locust_download_dir, exist_ok=True)
        os.makedirs(spark_upload_dir, exist_ok=True)
        os.makedirs(spark_run_dir, exist_ok=True)
        os.makedirs(spark_download_dir, exist_ok=True)
        # Exposed configuration
        self.SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(
            Path(basedir, "database.db").absolute()
        )
        self.LOCUST_UPLOAD_DIR = locust_upload_dir
        self.LOCUST_RUN_DIR = locust_run_dir
        self.LOCUST_DOWNLOAD_DIR = locust_download_dir
        self.SPARK_UPLOAD_DIR = spark_upload_dir
        self.SPARK_RUN_DIR = spark_run_dir
        self.SPARK_DOWNLOAD_DIR = spark_download_dir


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
