from datetime import datetime
import re

import logging
logger = logging.getLogger(__name__)

SHEET_NAME_MSK_2024 = "Москва"
SHEET_NAME_SPB_2024 = "Санкт-Петербург"
SHEET_NAME_KL_2024 = "Калининград"
SHEET_NAME_ROS_2024 = "Ростов-на-Дону"
SHEET_NAME_SAM_2024 = "Самара"
SHEET_NAME_EKB_2024 = "Екатеринбург"
SHEET_NAME_TU_2024 = "Тюмень"
SHEET_NAME_NOV_2024 = "Новосибирск"
SHEET_NAME_KR_2024 = "Красноярск"
SHEET_NAME_IR_2024 = "Иркутск"
SHEET_NAME_JA_2024 = "Якутск"
SHEET_NAME_MA_2024 = "Магадан"
SHEET_NAME_HA_2024 = "Хабаровск"
SHEET_NAME_SF_2024 = "Симферополь"

COL_REGION = "Регион"
COL_DATE = "Дата"
COL_FLIGHT = "Рейс"
COL_BOARD = "Борт"
COL_TYPE = "Тип ВС"
COL_DEP = "Т выл.факт"
COL_ARR = "Т пос.факт"
COL_APB = "АРВ"
COL_AB = "А/В"
COL_ARP="АРП"
COL_AP = "А/П"
COL_ROUTE="Маршрут"

DATA_ROW = {
    COL_REGION: "", 
    COL_DATE: "", 
    COL_FLIGHT: "", 
    COL_BOARD: "",
    COL_TYPE: "",
    COL_DEP: "", 
    COL_ARR: "", 
    COL_APB: "",
    COL_AB: "",
    COL_ARP: "",
    COL_AP: "",
    COL_ROUTE: ""
}

def try_parse_datetime(date_string, row_name, sheet_name):
    date_format = "%Y-%m-%d %H:%M:%S" 
    try:
        parsed_datetime = datetime.strptime(date_string, date_format)
        return parsed_datetime
    except ValueError:
        logger.error(f"Failed to parse date: {date_string}, row_name: {row_name}, sheet_name: {sheet_name}")
        return None
def group_and_log(res, col, value, row_name, sheet_name):
    if value:
        res[col] = value.group(1).strip()
    else:
        res[col] = None
        logger.warning(f"{col} not found in the row: {row_name}, sheet_name: {sheet_name}")

def set_and_log(res, col, value, row_name, sheet_name):
    if value:
        res[col] = value.removeprefix('-')
    else:
        res[col] = None
        logger.warning(f"{col} not found in the row: {row_name}, sheet_name: {sheet_name}")

def set_from_shr(res, shr, row_name, sheet_name):
    shr = shr.replace("_x000D_", "") # fixup for Magadan 2024
    shr_list = shr.split('\n')

    dof = re.search(r'DOF/(\d{6})', shr)
    group_and_log(res, COL_DATE, dof, row_name, sheet_name)

    flight_id = re.search(r'SHR-([^\n]+)', shr)
    group_and_log(res, COL_FLIGHT, flight_id, row_name, sheet_name)

    board = re.search(r'REG/([^\s]+)', shr)
    group_and_log(res, COL_BOARD, board, row_name, sheet_name)

    flight_type = re.search(r'TYP/([^\s]+)', shr)
    group_and_log(res, COL_TYPE, flight_type, row_name, sheet_name)

    zzzzdddd = r"^-(?=(?:.*[a-zA-Z]){4})(?=(?:.*\d){4})[a-zA-Z\d]{8}$"
    # shr_cut = [(idx, t.strip()) for idx, t in enumerate(shr_list) if len(t.strip()) == 9 and t.startswith("-")]
    shr_cut = [(idx, t.strip()) for idx, t in enumerate(shr_list) if bool(re.match(zzzzdddd, t.strip())) and t.startswith("-")]
    # logger.info(shr_cut)
    # logger.info(shr_list)
    # exit()
    # print(shr_cut, shr_cut[0][1]) [(1, '-ZZZZ0705')] -ZZZZ0705
    if len(shr_cut) == 2:
        set_and_log(res, COL_AB, shr_cut[0][1][:5], row_name, sheet_name)
        set_and_log(res, COL_DEP, shr_cut[0][1][5:], row_name, sheet_name)
        set_and_log(res, COL_AP, shr_cut[1][1][:5], row_name, sheet_name)
        set_and_log(res, COL_ARR, shr_cut[1][1][5:], row_name,sheet_name)
        route_idx = shr_cut[0][0] + 1
        route = shr_list[route_idx]
        set_and_log(res, COL_ROUTE, route, row_name, sheet_name)
    elif len(shr_cut) == 1:
        set_and_log(res, COL_AB, shr_cut[0][1][:5], row_name, sheet_name)
        set_and_log(res, COL_DEP, shr_cut[0][1][5:], row_name, sheet_name)
        set_and_log(res, COL_AP, None, row_name, sheet_name)
        set_and_log(res, COL_ARR, None, row_name, sheet_name)
        route_idx = shr_cut[0][0] + 1
        route = shr_list[route_idx]
        set_and_log(res, COL_ROUTE, route, row_name, sheet_name)
    else:
        set_and_log(res, COL_AB, None, row_name, sheet_name)
        set_and_log(res, COL_DEP, None, row_name, sheet_name)
        set_and_log(res, COL_AP, None, row_name, sheet_name)
        set_and_log(res, COL_ARR, None, row_name, sheet_name)
        logger.warning(f"{COL_DEP} and {COL_ARR} not found in the row: {row_name}, sheet_name: {sheet_name}")

    dep_coordinates_match = re.search(r'DEP/(\d\w\d+\w\d+\w)', shr)
    group_and_log(res, COL_APB, dep_coordinates_match, row_name, sheet_name)

    dest_coordinates_match = re.search(r'DEST/(\d\w\d+\w\d+\w)', shr)
    group_and_log(res, COL_ARP, dest_coordinates_match, row_name, sheet_name)

def set_from_pln(res, pln, row_name, sheet_name):
    if (pln == "nan"):
        return 
    
    pln_list = pln.split('-')

    dof = re.search(r'DOF/(\d{6})', pln)
    group_and_log(res, COL_DATE, dof, row_name, sheet_name)

    if (len(pln_list) > 0):
        flight_id = pln_list[1]
        set_and_log(res, COL_FLIGHT, flight_id, row_name, sheet_name)

    if (len(pln_list) > 1):
        board = pln_list[2]
        set_and_log(res, COL_BOARD, board, row_name, sheet_name)

    dep_coordinates_match = re.search(r'DEP/(\d\w\d+\w\d+\w)', pln)
    group_and_log(res, COL_APB, dep_coordinates_match, row_name, sheet_name)

    dest_coordinates_match = re.search(r'DEST/(\d\w\d+\w\d+\w)', pln)
    group_and_log(res, COL_ARP, dest_coordinates_match, row_name, sheet_name)
