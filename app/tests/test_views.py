import pytest


@pytest.mark.parametrize('test_input,expected_day,description', [
    ('Dawngate/2023/11', 12, "Normal flow"),
    ('Dawngate/2023/1', 31, "Single digit month"),
    ('Are_You_the_One%3F/2022/10', 11, "Non-URI safe character")
])
def test_top_day_for_article_in_month(client, test_input, expected_day, description):
    response = client.get('/api/v1/views/top-day/' + test_input)
    assert response.json["day"] == expected_day, description


@pytest.mark.parametrize('test_input,expected_status,description', [
    ('Dawngate/5000/10', 400, "Date in the future"),
    ('Dawngate/50000/10', 400, "Year out of range"),
    ('Dawngate/2000/20', 400, "Month out of range"),
    ('fake_article_name/2023/1', 404, "Article that does not exist")
])
def test_top_day_for_article_in_month_errors(client, test_input, expected_status, description):
    response = client.get('/api/v1/views/top-day/' + test_input)
    assert response.status_code == expected_status


def test_views_for_article_in_week(client):
    response = client.get('/api/v1/views/article/week/Dawngate/2023/1')
    assert response.json["views"] == 129


def test_views_for_article_in_month(client):
    response = client.get('/api/v1/views/article/month/Dawngate/2023/1')
    assert response.json["views"] == 600


def test_top_articles_for_month(client):
    response = client.get('/api/v1/views/top-articles/month/2023/1')
    assert False


def test_top_articles_for_week(client):
    response = client.get('/api/v1/views/top-articles/week/2023/1')
    assert False
