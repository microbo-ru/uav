import re
from typing import Any
import random
import datetime
from parser_common import set_from_shr
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

def parser_2025(row):
    # logger.info(row)

    res = DATA_ROW.copy()
    res[COL_REGION] = row['Центр ЕС ОрВД']

    shr = row['SHR']

    set_from_shr(res, shr, row.name, "2025")

    return res
