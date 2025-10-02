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
COL_ROUTE, \
SHEET_NAME_ROS_2024

import logging
logger = logging.getLogger(__name__)

def parser_2024_ros(row):
    # logger.info(row)

    res = DATA_ROW.copy()
    res[COL_REGION] = SHEET_NAME_ROS_2024

    if row["Дата"] == 3:
        return res
    if row["Дата"] == None:
        return res

    res[COL_DATE] = row["Дата"]
    res[COL_FLIGHT] = row["Рейс"]
    res[COL_BOARD] = row["Борт"]
    # res[COL_TYPE] = row[COL_TYPE]
    res[COL_DEP] = row["Т выл. факт"]
    res[COL_ARR] = row["Т пос. факт"]
    res[COL_APB] = row["А/В название"]
    # res[COL_AB] = row[COL_AB]
    res[COL_ARP] = row["А/Н название"]
    # res[COL_AP] = row[COL_AP]
    res[COL_ROUTE] = row["Маршрут"]

    return res
