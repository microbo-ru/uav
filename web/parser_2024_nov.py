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
SHEET_NAME_NOV_2024

import logging
logger = logging.getLogger(__name__)

def parser_2024_nov(row):
    # logger.info(row)
    res = DATA_ROW.copy()
    res[COL_REGION] = SHEET_NAME_NOV_2024
    # res[COL_DATE] = try_parse_datetime(str(row[COL_DATE]))
    res[COL_FLIGHT] = row["Рейс"]
    res[COL_BOARD] = row["Борт. номер ВС."]
    res[COL_TYPE] = row["Тип/ группа ВС"]
    res[COL_DEP] = row["Время вылета факт."]
    res[COL_ARR] = row["Время посадки факт."]
    res[COL_APB] = row["АФТН АП вылета"]
    # res[COL_AB] = row[COL_AB]
    res[COL_ARP] = row["АФТН АП посадки"]
    # res[COL_AP] = row[COL_AP]
    res[COL_ROUTE] = row["Текст исходного маршрута"]

    return res
