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

def parse_atc_plan(atc_plan: str) -> dict[str, str]:
    """Parse an ATC flight plan string into a dictionary.

    The route string is not converted to lat/lon in this process.

    Parameters
    ----------
    atc_plan : str
        An ATC flight plan string conforming to ICAO Doc 4444-ATM/501 (Appendix 2)

    Returns
    -------
    dict[str, str]
        A dictionary consisting of parsed components of the ATC flight plan.
        A full ATC plan will contain the keys:

        - ``callsign``: ICAO flight callsign
        - ``flight_rules``: Flight rules ("I", "V", "Y", "Z")
        - ``type_of_flight``: Type of flight ("S", "N", "G", "M", "X")
        - ``number_aircraft``: The number of aircraft, if more than one
        - ``type_of_aircraft``: ICAO aircraft type
        - ``wake_category``: Wake turbulence category
        - ``equipment``: Radiocommunication, navigation and approach aid equipment and capabilities
        - ``transponder``: Surveillance equipment and capabilities
        - ``departure_icao``: ICAO departure airport
        - ``time``: Estimated off-block (departure) time (UTC)
        - ``speed_type``: Speed units ("K": km / hr, "N": knots)
        - ``speed``: Cruise true airspeed in ``speed_type`` units
        - ``level_type``: Level units ("F", "S", "A", "M")
        - ``level``: Cruise level
        - ``route``: Route string
        - ``destination_icao``: ICAO destination airport
        - ``duration``: The total estimated elapsed time for the flight plan
        - ``alt_icao``: ICAO alternate destination airport
        - ``second_alt_icao``: ICAO second alternate destination airport
        - ``other_info``: Other information
        - ``supplementary_info``: Supplementary information

    References
    ----------
    - https://applications.icao.int/tools/ATMiKIT/story_content/external_files/story_content/external_files/DOC%204444_PANS%20ATM_en.pdf

    See Also
    --------
    :func:`to_atc_plan`
    """
    atc_plan = atc_plan.replace("\r", " ")
    atc_plan = atc_plan.replace("\n", " ")
    atc_plan = atc_plan.upper()
    atc_plan = atc_plan.strip()

    if len(atc_plan) == 0:
        raise ValueError("Empty or invalid flight plan")

    atc_plan = atc_plan.replace("(FPL", "")
    atc_plan = atc_plan.replace(")", "")
    atc_plan = atc_plan.replace("--", "-")

    basic = atc_plan.split("-")
    print(basic)

    flightplan: dict[str, Any] = {}

    # Callsign
    if len(basic) > 1:
        flightplan["callsign"] = basic[1]

    # Flight Rules
    if len(basic) > 2:
        flightplan["flight_rules"] = basic[2][0]
        flightplan["type_of_flight"] = basic[2][1]

    # Aircraft
    if len(basic) > 3:
        aircraft = basic[3].split("/")
        matches = re.match(r"(\d{1})(\S{3,4})", aircraft[0])
        groups = matches.groups() if matches else ()

        if matches and len(groups) > 2:
            flightplan["number_aircraft"] = groups[1]
            flightplan["type_of_aircraft"] = groups[2]
        else:
            flightplan["type_of_aircraft"] = aircraft[0]

        if len(aircraft) > 1:
            flightplan["wake_category"] = aircraft[1]

    # Equipment
    if len(basic) > 4:
        equip = basic[4].split("/")
        flightplan["equipment"] = equip[0]
        if len(equip) > 1:
            flightplan["transponder"] = equip[1]

    # Dep. airport info
    if len(basic) > 5:
        matches = re.match(r"(\D*)(\d*)", basic[5])
        groups = matches.groups() if matches else ()

        if groups:
            flightplan["departure_icao"] = groups[0]
        if len(groups) > 1:
            flightplan["time"] = groups[1]

    # Speed and route info
    if len(basic) > 6:
        matches = re.match(r"(\D*)(\d*)(\D*)(\d*)", basic[6])
        groups = matches.groups() if matches else ()

        # match speed and level
        if groups:
            flightplan["speed_type"] = groups[0]
            if len(groups) > 1:
                flightplan["speed"] = groups[1]
            if len(groups) > 2:
                flightplan["level_type"] = groups[2]
            if len(groups) > 3:
                flightplan["level"] = groups[3]

            flightplan["route"] = basic[6][len("".join(groups)) :].strip()
        else:
            flightplan["route"] = basic[6].strip()

    # Dest. airport info
    if len(basic) > 7:
        matches = re.match(r"(\D{4})(\d{4})", basic[7])
        groups = matches.groups() if matches else ()

        if groups:
            flightplan["destination_icao"] = groups[0]
        if len(groups) > 1:
            flightplan["duration"] = groups[1]

        matches = re.match(r"(\D{4})(\d{4})(\s{1})(\D{4})", basic[7])
        groups = matches.groups() if matches else ()

        if len(groups) > 3:
            flightplan["alt_icao"] = groups[3]

        matches = re.match(r"(\D{4})(\d{4})(\s{1})(\D{4})(\s{1})(\D{4})", basic[7])
        groups = matches.groups() if matches else ()

        if len(groups) > 5:
            flightplan["second_alt_icao"] = groups[5]

    # Other info
    if len(basic) > 8:
        info = basic[8]
        idx = info.find("DOF")
        if idx != -1:
            flightplan["departure_date"] = info[idx + 4 : idx + 10]

        flightplan["other_info"] = info.strip()

    # Supl. Info
    if len(basic) > 9:
        sup_match = re.findall(r"(\D{1}[\/]{1})", basic[9])
        if sup_match:
            suplInfo = {}
            for i in range(len(sup_match) - 1):
                this_key = sup_match[i]
                this_idx = basic[9].find(this_key)

                next_key = sup_match[i + 1]
                next_idx = basic[9].find(next_key)

                val = basic[9][this_idx + 2 : next_idx - 1]
                suplInfo[this_key[0]] = val

            last_key = sup_match[-1]
            last_idx = basic[9].find(last_key)
            suplInfo[last_key[0]] = basic[9][last_idx + 2 :]

            flightplan["supplementary_info"] = suplInfo

    return flightplan

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
