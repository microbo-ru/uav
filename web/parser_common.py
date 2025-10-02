from datetime import datetime
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
    COL_ROUTE: "undefined"
}

def try_parse_datetime(date_string, row_name, sheet_name):
    date_format = "%Y-%m-%d %H:%M:%S" 
    try:
        parsed_datetime = datetime.strptime(date_string, date_format)
        return parsed_datetime
    except ValueError:
        logger.error(f"Failed to parse date: {date_string}, row_name: {row_name}, sheet_name: {sheet_name}")
        return None