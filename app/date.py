import calendar
import datetime
from typing import Tuple


def get_datetime_range_for_month(year: int, month: int) -> Tuple[str, str]:
    last_day = calendar.monthrange(year, month)[1]
    start_date = datetime.datetime(year, month, 1)
    end_date = datetime.datetime(year, month, last_day)
    formatted_start = start_date.strftime("%Y%m%d")
    formatted_end = end_date.strftime("%Y%m%d")
    return formatted_start, formatted_end


def get_datetime_range_for_week(year: int, week: int) -> Tuple[str, str]:
    start_date = datetime.date.fromisocalendar(year, week, 1)
    end_date = datetime.date.fromisocalendar(year, week, 7)
    formatted_start = start_date.strftime("%Y%m%d")
    formatted_end = end_date.strftime("%Y%m%d")
    return formatted_start, formatted_end
