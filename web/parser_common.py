from datetime import datetime
import logging
logger = logging.getLogger(__name__)

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
# COL_FIELD18="Поле 18"

DATA_ROW = {
    COL_REGION: "undefined", 
    COL_DATE: "undefined", 
    COL_FLIGHT: "undefined", 
    COL_BOARD: "undefined",
    COL_TYPE: "undefined",
    COL_DEP: "undefined", 
    COL_ARR: "undefined", 
    COL_APB: "undefined",
    COL_AB: "undefined",
    COL_ARP: "undefined",
    COL_AP: "undefined",
    COL_ROUTE: "undefined",
    "name": "undefined"
    # COL_FIELD18: "undefined"
}

def try_parse_datetime(date_string):
    date_format = "%Y-%m-%d %H:%M:%S" 
    try:
        parsed_datetime = datetime.strptime(date_string, date_format)
        return parsed_datetime
    except ValueError:
        logger.error(f"Failed to parse date: {date_string}")
        return None