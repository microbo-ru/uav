from parser_common import set_from_pln
from parser_common import try_parse_datetime,\
DATA_ROW, \
COL_REGION, \
SHEET_NAME_HA_2024

import logging
logger = logging.getLogger(__name__)

def parser_2024_ha(row):
    # logger.info(row)
    res = DATA_ROW.copy()
    res[COL_REGION] = SHEET_NAME_HA_2024

    pln = str(row['Телеграмма PLN'])
    set_from_pln(res, pln, row.name, SHEET_NAME_HA_2024)
    

    return res
