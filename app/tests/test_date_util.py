import app.date_util as date_util


def test_get_datetime_range_for_month(client):
    actual = date_util.get_datetime_range_for_month(2023, 11)
    expected = ('20231101', '20231130')
    assert actual == expected


def test_get_datetime_range_for_week(client):
    actual = date_util.get_datetime_range_for_week(2022, 1)
    expected = ('20220103', '20220109')
    assert actual == expected


def test_get_dates_for_week(client):
    actual = date_util.get_dates_for_week(2023, 2)
    assert len(actual) == 7
    assert actual[0].day == 9
    assert actual[6].day == 15
