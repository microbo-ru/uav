import re
from typing import Any
from parser_common import DATA_ROW, \
COL_REGION, \
COL_DATE, \
COL_FLIGHT, \
COL_BOARD, \
COL_TYPE, \
COL_DEP, \
COL_ARR, \
COL_APB, \
COL_AB, \
COL_ARP, \
COL_AP, \
COL_ROUTE, \
COL_FIELD18

import logging
logger = logging.getLogger(__name__)

def parser_2024_msk(row):
    logger.info(row)
    DATA_ROW[COL_REGION] = "Москва"
    DATA_ROW[COL_DATE] = row["Дата полёта"]
    # DATA_ROW[COL_FLIGHT] = row[COL_FLIGHT]
    # DATA_ROW[COL_BOARD] = row[COL_BOARD]
    # DATA_ROW[COL_TYPE] = row[COL_TYPE]
    # DATA_ROW[COL_DEP] = row[COL_DEP]
    # DATA_ROW[COL_ARR] = row[COL_ARR]
    # DATA_ROW[COL_APB] = row[COL_APB]
    # DATA_ROW[COL_AB] = row[COL_AB]
    # DATA_ROW[COL_ARP] = row[COL_ARP]
    # DATA_ROW[COL_AP] = row[COL_AP]
    # DATA_ROW[COL_ROUTE] = row[COL_ROUTE]
    # DATA_ROW[COL_FIELD18] = row[COL_FIELD18]

    return DATA_ROW
