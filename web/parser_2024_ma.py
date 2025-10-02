from parser_common import set_from_shr
from parser_common import try_parse_datetime,\
DATA_ROW, \
COL_REGION, \
SHEET_NAME_MA_2024

import logging
logger = logging.getLogger(__name__)

def parser_2024_ma(row):
    # logger.info(row)
    
    res = DATA_ROW.copy()
    res[COL_REGION] = SHEET_NAME_MA_2024

    shr = str(row['Планы полета БВС'])
    set_from_shr(res, shr, row.name, SHEET_NAME_MA_2024)

    return res
