import re
from typing import Any
import random
import datetime

# https://github.com/contrailcirrus/pycontrails/blob/main/pycontrails/core/flightplan.py
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
COL_ROUTE

import logging
logger = logging.getLogger(__name__)

def group_and_log(res, col, value, row_name):
    if value:
        res[col] = value.group(1)
    else:
        res[col] = None
        logger.warning(f"{col} not found in the row: {row_name}")

def set_and_log(res, col, value, row_name):
    if value:
        res[col] = value.removeprefix('-')
    else:
        res[col] = None
        logger.warning(f"{col} not found in the row: {row_name}")

def parser_2025(row):
    # logger.info(row)

    res = DATA_ROW.copy()
    res[COL_REGION] = row['Центр ЕС ОрВД']

    shr = row['SHR']
    shr_list = shr.split('\n')

    dof = re.search(r'DOF/(\d{6})', shr)
    group_and_log(res, COL_DATE, dof, row.name)

    flight_id = re.search(r'SHR-([^\n]+)', shr)
    group_and_log(res, COL_FLIGHT, flight_id, row.name)

    board = re.search(r'REG/([^\s]+)', shr)
    group_and_log(res, COL_BOARD, board, row.name)

    flight_type = re.search(r'TYP/([^\s]+)', shr)
    group_and_log(res, COL_TYPE, flight_type, row.name)

    shr_cut = [(idx, t) for idx, t in enumerate(shr_list) if len(t) == 9 and t.startswith("-")]
    # print(shr_cut, shr_cut[0][1]) [(1, '-ZZZZ0705')] -ZZZZ0705
    if len(shr_cut) == 2:
        set_and_log(res, COL_AB, shr_cut[0][1][:5], row.name)
        set_and_log(res, COL_DEP, shr_cut[0][1][5:], row.name)
        set_and_log(res, COL_AP, shr_cut[1][1][:5], row.name)
        set_and_log(res, COL_ARR, shr_cut[1][1][5:], row.name)
        route_idx = shr_cut[0][0] + 1
        route = shr_list[route_idx]
        set_and_log(res, COL_ROUTE, route, row.name)
    elif len(shr_cut) == 1:
        set_and_log(res, COL_AB, shr_cut[0][1][:5], row.name)
        set_and_log(res, COL_DEP, shr_cut[0][1][5:], row.name)
        set_and_log(res, COL_AP, None, row.name)
        set_and_log(res, COL_ARR, None, row.name)
        route_idx = shr_cut[0][0] + 1
        route = shr_list[route_idx]
        set_and_log(res, COL_ROUTE, route, row.name)
    else:
        logger.warning(f"{COL_DEP} and {COL_ARR} not found in the row: {row.name}")

    dep_coordinates_match = re.search(r'DEP/(\d\w\d+\w\d+\w)', shr)
    group_and_log(res, COL_APB, dep_coordinates_match, row.name)

    dest_coordinates_match = re.search(r'DEST/(\d\w\d+\w\d+\w)', shr)
    group_and_log(res, COL_ARP, dest_coordinates_match, row.name)

    return res
