from parser_common import set_from_shr
from parser_common import DATA_ROW, \
COL_REGION, \
COL_DATE, \
SHEET_NAME_MSK_2024

import logging
logger = logging.getLogger(__name__)

def parser_2024_msk(row):
    # logger.info(row)
    res = DATA_ROW.copy()
    res[COL_REGION] = SHEET_NAME_MSK_2024
    res[COL_DATE] = row["Дата полёта"]

    shr = str(row['Сообщение SHR'])
    set_from_shr(res, shr, row.name, SHEET_NAME_MSK_2024)

    return res
