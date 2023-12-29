import datetime
import pytest

import app.date_util as date_util
from app.exceptions import ValidationError


def test_get_month_range(client):
    actual_range = date_util.get_month_range(2023, 11)
    assert actual_range[0] == datetime.date(2023, 11, 1)
    assert actual_range[1] == datetime.date(2023, 11, 30)


def test_get_month_range_errors(client):
    with pytest.raises(ValidationError):
        date_util.get_month_range(11000, 11)
    with pytest.raises(ValidationError):
        date_util.get_month_range(2023, 15)


def test_get_week_range(client):
    actual_range = date_util.get_week_range(2022, 3)
    assert actual_range[0] == datetime.date(2022, 1, 17)
    assert actual_range[1] == datetime.date(2022, 1,  23)


def test_get_week_range_errors(client):
    with pytest.raises(ValidationError):
        date_util.get_week_range(11000, 11)
    with pytest.raises(ValidationError):
        date_util.get_week_range(2023, 54)


def test_get_dates_for_week(client):
    actual = date_util.get_dates_for_week(2023, 2)
    assert len(actual) == 7
    assert actual[0] == datetime.date(2023,1, 9)
    assert actual[6] == datetime.date(2023, 1, 15)


def test_verify_date_in_past(client):
    date_util.verify_date_in_past(datetime.date(2023, 1, 1))
    with pytest.raises(ValidationError):
        date_util.verify_date_in_past(datetime.date(5000, 1, 1))
