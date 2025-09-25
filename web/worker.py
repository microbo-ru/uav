import os
import shutil
import json

import pandas as pd
from pathlib import Path

from celery import Celery
from celery import current_task


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task(name="create_task")
def create_task():
    return True

@celery.task(name="terminate_task")
def terminate_task(task_id):
    return True
