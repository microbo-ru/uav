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
SHEET_NAME_SF_2024

import logging
logger = logging.getLogger(__name__)

def parser_2024_sf(row):
    # logger.info(row)
    res = DATA_ROW.copy()
    res[COL_REGION] = SHEET_NAME_SF_2024
    # res[COL_DATE] = try_parse_datetime(str(row[COL_DATE]))
    # res[COL_FLIGHT] = row[COL_FLIGHT]
    # res[COL_BOARD] = row[COL_BOARD]
    # res[COL_TYPE] = row[COL_TYPE]
    # res[COL_DEP] = row[COL_DEP]
    # res[COL_ARR] = row[COL_ARR]
    # res[COL_APB] = row[COL_APB]
    # res[COL_AB] = row[COL_AB]
    # res[COL_ARP] = row[COL_ARP]
    # res[COL_AP] = row[COL_AP]
    # res[COL_ROUTE] = row[COL_ROUTE]

    return res
