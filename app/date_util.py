import calendar
import datetime
from typing import Tuple, List
from app.exceptions import ValidationError


def validate_month(year: int, month: int) -> datetime.date:
    try:
        input_date = datetime.date(year, month, 1)
    except ValueError:
        raise ValidationError('Invalid year or month provided')
    return input_date


def validate_date_in_past(date: datetime.date):
    if date > datetime.date.today():
        raise ValidationError("Date information provided must be in the past")


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


def get_dates_for_week(year: int, week: int) -> List[datetime.date]:
    dates = []
    for day in range(1, 8):
        dates.append(datetime.date.fromisocalendar(year, week, day))
    return dates
