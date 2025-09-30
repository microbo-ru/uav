import re
from typing import Any
from parser_common import DATA_ROW, COL_REGION, COL_FLIGHT, COL_BOARD

import logging
logger = logging.getLogger(__name__)

def parser_2024(row):
    DATA_ROW[COL_REGION] = "Москва"
    DATA_ROW[COL_FLIGHT] = "TBD 1"
    DATA_ROW[COL_BOARD] = "TBD 2"

    return DATA_ROW
