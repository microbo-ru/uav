import re
from parser_common import try_parse_datetime,\
DATA_ROW, \
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
COL_ROUTE,\
SHEET_NAME_SAM_2024

import logging
logger = logging.getLogger(__name__)

def parser_2024_sam(row):
    # logger.info(row)
    res = DATA_ROW.copy()
    res[COL_REGION] = SHEET_NAME_SAM_2024
    # res[COL_DATE] = row["Дата, время вылета"]
    # res[COL_FLIGHT] = row[COL_FLIGHT]
    # res[COL_BOARD] = row[COL_BOARD]
    # res[COL_TYPE] = row[COL_TYPE]
    res[COL_DEP] = row["Дата, время вылета"]
    res[COL_ARR] = row["Дата, время посадки"]
    res[COL_APB] = row["Место вылета"]
    # res[COL_AB] = row[COL_AB]
    res[COL_ARP] = row["Место посадки"]
    # res[COL_AP] = row[COL_AP]
    res[COL_ROUTE] = row["Район работы"]

    return res
