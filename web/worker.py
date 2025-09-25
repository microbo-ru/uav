import os
import shutil
import json

import pandas as pd
from pathlib import Path
import logging

from celery import Celery
from celery import current_task
import time

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
logger = logging.getLogger('celery.task')

@celery.task(name="create_task")
def create_task(path):
    logger.info("Executing create_task with id: %s and path %s", create_task.request.id, path)

    time.sleep(60) #sec
    return True

@celery.task(name="terminate_task")
def terminate_task(task_id):
    return True
