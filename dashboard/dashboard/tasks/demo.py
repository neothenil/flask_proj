import os
import time
from random import random

from . import celery


@celery.task(bind=True)
def add(self, a, b):
    self.update_state(state="PENDING", meta={"pid": os.getpid()})
    if random() < 0.3:
        raise RuntimeError("Failed to execute task `add`")
    time.sleep(5)
    self.update_state(state="START", meta={"new_data": "test"})
    time.sleep(5)
    return a + b
