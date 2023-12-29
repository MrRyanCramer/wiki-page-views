import calendar
import datetime
from typing import Tuple, List
from app.exceptions import ValidationError


def get_month_range(year: int, month: int) -> Tuple[datetime.date, datetime.date]:
    try:
        last_day_number_for_month = calendar.monthrange(year, month)[1]
        return (
            datetime.date(year, month, 1),
            datetime.date(year, month, last_day_number_for_month)
        )
    except ValueError:
        raise ValidationError('Invalid year or month provided')


def get_week_range(year: int, week: int) -> Tuple[datetime.date, datetime.date]:
    try:
        return (
            datetime.date.fromisocalendar(year, week, 1),
            datetime.date.fromisocalendar(year, week, 7)
        )
    except ValueError:
        raise ValidationError('Invalid year or week provided')


def verify_date_in_past(date: datetime.date):
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
