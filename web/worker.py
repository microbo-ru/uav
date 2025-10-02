import os
import shutil
import json

import pandas as pd
from pathlib import Path
import logging

from celery import Celery
from celery import current_task
import time
from pathlib import Path
from parser_2025 import parser_2025
from parser_2024_msk import parser_2024_msk
from parser_2024_spb import parser_2024_spb
from parser_2024_ekb import parser_2024_ekb
from parser_2024_ha import parser_2024_ha
from parser_2024_ir import parser_2024_ir
from parser_2024_ja import parser_2024_ja
from parser_2024_kl import parser_2024_kl
from parser_2024_kr import parser_2024_kr
from parser_2024_ma import parser_2024_ma
from parser_2024_nov import parser_2024_nov
from parser_2024_ros import parser_2024_ros
from parser_2024_sam import parser_2024_sam
from parser_2024_sf import parser_2024_sf
from parser_2024_tu import parser_2024_tu

from parser_common import SHEET_NAME_MSK_2024, \
SHEET_NAME_SPB_2024, SHEET_NAME_KL_2024, SHEET_NAME_ROS_2024, SHEET_NAME_SAM_2024,\
SHEET_NAME_EKB_2024, SHEET_NAME_TU_2024, SHEET_NAME_NOV_2024, \
SHEET_NAME_KR_2024, SHEET_NAME_IR_2024, SHEET_NAME_JA_2024, SHEET_NAME_MA_2024, \
SHEET_NAME_HA_2024, SHEET_NAME_SF_2024

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
logger = logging.getLogger('celery.task')

def get_parser(sheet_name, df_head):
    # logger.info(df_head)
    head_as_string = df_head.to_string()

    if sheet_name in [SHEET_NAME_MSK_2024]:
        return lambda t: parser_2024_msk(t), 1
    if sheet_name in [SHEET_NAME_SPB_2024]:
        return lambda t: parser_2024_spb(t), 0
    if sheet_name in [SHEET_NAME_KL_2024]:
        return lambda t: parser_2024_kl(t), 0
    if sheet_name in [SHEET_NAME_ROS_2024]:
        return lambda t: parser_2024_ros(t), 1 # rows to skip
    if sheet_name in [SHEET_NAME_SAM_2024]:
        return lambda t: parser_2024_sam(t), 0
    if sheet_name in [SHEET_NAME_EKB_2024]:
        return lambda t: parser_2024_ekb(t), 0
    if sheet_name in [SHEET_NAME_TU_2024]:
        return lambda t: parser_2024_tu(t), 0
    if sheet_name in [SHEET_NAME_NOV_2024]:
        return lambda t: parser_2024_nov(t), 0
    if sheet_name in [SHEET_NAME_KR_2024]:
        return lambda t: parser_2024_kr(t), 0
    if sheet_name in [SHEET_NAME_IR_2024]:
        return lambda t: parser_2024_ir(t), 0
    if sheet_name in [SHEET_NAME_JA_2024]:
        return lambda t: parser_2024_ja(t), 0
    if sheet_name in [SHEET_NAME_MA_2024]:
        return lambda t: parser_2024_ma(t), 2
    if sheet_name in [SHEET_NAME_HA_2024]:
        return lambda t: parser_2024_ha(t), 1
    if sheet_name in [SHEET_NAME_SF_2024]:
        return lambda t: parser_2024_sf(t), 1
    elif "Центр ЕС ОрВД" in head_as_string:
        return lambda t: parser_2025(t), 0
    else:
        return None, None

@celery.task(name="create_task")
def create_task(path):
    logger.info("Executing create_task with id: %s and path %s", create_task.request.id, path)

    input_path = Path(path)
    output_path = input_path.with_suffix(".csv")
    xls = pd.ExcelFile(path)

    all_dataframes = []
    for sheet_name in xls.sheet_names:
        # safe_sheet_name = sheet_name.replace(" ", "_")
        # output_path1 = str(input_path.with_suffix(".csv"))
        # output_path1 = output_path1[:-4] + f"_{safe_sheet_name}" + output_path1[-4:]
        df = pd.read_excel(xls, sheet_name, nrows=3)
        parser, skiprows = get_parser(sheet_name, df)

        df = pd.read_excel(xls, sheet_name, skiprows=skiprows)

        if parser is not None:
            extracted_columns = df.apply(parser, axis=1, result_type="expand")
            # extracted_columns.to_csv(output_path1, index=False, encoding='utf-8-sig')
            all_dataframes.append(extracted_columns)
        else:
            logger.info("Parser not found: %s", sheet_name)

    final_df = pd.concat(all_dataframes)
    final_df.to_csv(str(output_path), index=False, encoding='utf-8-sig')

    return True

@celery.task(name="terminate_task")
def terminate_task(task_id):
    return True
