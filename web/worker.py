import os
import shutil
import json

import pandas as pd
from pathlib import Path
import logging

from celery import Celery
from celery import current_task
import time
from parser_2025 import parser_2025
from parser_2024_msk import parser_2024_msk
from parser_2024_spb import parser_2024_spb
from pathlib import Path

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
logger = logging.getLogger('celery.task')

def get_parser(sheet_name, df_head):
    # logger.info(df_head)

    head_as_string = df_head.to_string()
    if sheet_name in ["Москва", ""]:
        return lambda t: parser_2024_msk(t), 1
    if sheet_name in ["Санкт-Петербург"]:
        return lambda t: parser_2024_spb(t), 0
    elif "Центр ЕС ОрВД" in head_as_string:
        return lambda t: parser_2025(t), 0
    else:
        return None, None

@celery.task(name="create_task")
def create_task(path):
    logger.info("Executing create_task with id: %s and path %s", create_task.request.id, path)

    input_path = Path(path)
    xls = pd.ExcelFile(path)

    for sheet_name in xls.sheet_names[:2]:
        safe_sheet_name = sheet_name.replace(" ", "_")
        output_path = str(input_path.with_suffix(".csv"))
        output_path = output_path[:-4] + f"_{safe_sheet_name}" + output_path[-4:]
        # print(output_path)
        df = pd.read_excel(xls, sheet_name, nrows=3)
        parser, skiprows = get_parser(sheet_name, df)

        df = pd.read_excel(xls, sheet_name, skiprows=skiprows)

        if parser is not None:
            extracted_columns = df.apply(parser, axis=1, result_type="expand")
            extracted_columns.to_csv(output_path, index=False, encoding='utf-8-sig')
        else:
            logger.info("Parser not found")

    return True

@celery.task(name="terminate_task")
def terminate_task(task_id):
    return True
