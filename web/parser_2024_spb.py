import re
from typing import Any
from parser_common import DATA_ROW, COL_REGION, COL_FLIGHT, COL_BOARD

import logging
logger = logging.getLogger(__name__)

def parser_2024_spb(row):
    DATA_ROW[COL_REGION] = "Санкт-Петербург"
    DATA_ROW[COL_FLIGHT] = "TBD 3"
    DATA_ROW[COL_BOARD] = "TBD 4"
    
    return DATA_ROW
