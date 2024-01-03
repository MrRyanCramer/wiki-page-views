import pytest
import requests_mock as mocks

# Test fixtures
from app.tests.test_views_data import daily_views_for_article_in_month, daily_views_for_article_in_week, \
    top_articles, monthly_views_for_article

# Url constants
url_prefix = '/api/v1/views/'
top_day_base_url = url_prefix + 'top-day/'
weekly_article_views_base_url = url_prefix + 'article/week/'
monthly_article_views_base_url = url_prefix + 'article/month/'
top_articles_for_month_base_url = url_prefix + 'top-articles/month/'
top_articles_for_week_base_url = '/api/v1/views/top-articles/week/'


class TestPageViewIntegration:
    """Integration Tests for the page views api

    These tests will hit the actual wikipedia API, and are therefore more brittle and resource intensive than their
    mocked counterparts.
    """

    @pytest.mark.parametrize('test_input,expected_day,description', [
        ('Dawngate/2023/11', 12, 'Normal flow'),
        ('Dawngate/2023/1', 31, 'Single digit month'),
        ('Are_You_the_One%3F/2022/10', 11, 'Non-URI safe character')
    ])
    def test_top_day_for_article_in_month(self, client, test_input, expected_day, description):
        response = client.get(top_day_base_url + test_input)
        assert response.json['day'] == expected_day, description

    def test_views_for_article_in_week(self, client):
        response = client.get(weekly_article_views_base_url + 'Dawngate/2023/1')
        assert response.json['views'] == 129

    def test_views_for_article_in_month(self, client):
        response = client.get(monthly_article_views_base_url + 'Dawngate/2023/1')
        assert response.json['views'] == 600

    def test_top_articles_for_month(self, client):
        response = client.get(top_articles_for_month_base_url + '2023/1')
        articles = response.json['articles']
        assert len(articles) == 1000
        assert articles[0] == {'article': 'Main_Page', 'rank': 1, 'views': 153563201}
        assert articles[1] == {'article': 'Special:Search', 'rank': 2, 'views': 41184546}

    def test_top_articles_for_week(self, client):
        response = client.get(top_articles_for_week_base_url + '2023/1')
        articles = response.json['articles']
        assert len(articles) == 1000
        assert articles[0] == {'article': 'Main_Page', 'rank': 1, 'views': 33951684}
        assert articles[1] == {'article': 'Special:Search', 'rank': 2, 'views': 8984262}


class TestPageViewMocked:
    """ Unit tests for the page views api

    These tests utilize mocking to remove the dependency on the wikipedia API, using sample data instead"""

    @pytest.mark.parametrize('service_status_code,expected_status,expected_error,description', [
        (400, 500, 'internal server error', 'Service responds with 400'),
        (404, 404, 'not found', 'Service responds with 404'),
        (500, 500, 'internal server error', 'Service responds with 500')
    ])
    def test_service_error_responses(self, client, requests_mock, service_status_code, expected_status, expected_error,
                                     description):
        """Tests the cases where the service responds with an error code"""
        requests_mock.get(mocks.ANY, status_code=service_status_code)
        response = client.get(top_day_base_url + 'fake_article_name/2023/1')
        assert response.status_code == expected_status, description
        assert response.json['error'] == expected_error, description

    @pytest.mark.parametrize('test_url,expected_status,description', [
        (top_day_base_url + 'Dawngate/5000/10', 400, 'Date in the future'),
        (top_day_base_url + 'Dawngate/50000/10', 400, 'Year out of range'),
        (top_day_base_url + 'Dawngate/2000/20', 400, 'Month out of range'),
        (weekly_article_views_base_url + 'Dawngate/2022/54', 400, 'Week number out of range')
    ])
    def test_bad_date_validation(self, client, requests_mock, daily_views_for_article_in_month,
                                 test_url, expected_status, description):
        """Tests error case handling for bad dates"""
        requests_mock.get(mocks.ANY, json={})
        response = client.get(test_url)
        assert response.status_code == expected_status, description

    def test_top_day_for_article_in_month(self, client, requests_mock, daily_views_for_article_in_month):
        """Tests the happy path for top day for article"""
        requests_mock.get(mocks.ANY, json=daily_views_for_article_in_month)
        response = client.get(top_day_base_url + 'Dawngate/2023/11')
        assert response.json['day'] == 12

    def test_views_for_article_in_week(self, client, requests_mock, daily_views_for_article_in_week):
        """Tests the happy path for views for article in week"""
        requests_mock.get(mocks.ANY, json=daily_views_for_article_in_week)
        response = client.get(weekly_article_views_base_url + 'Dawngate/2023/45')
        assert response.json['views'] == 5023

    def test_views_for_article_in_month(self, client, requests_mock, monthly_views_for_article):
        """Tests the happy path for article views per month"""
        requests_mock.get(mocks.ANY, json=monthly_views_for_article)
        response = client.get(monthly_article_views_base_url + 'Dawngate/2023/1')
        assert response.json['views'] == 600

    def test_top_articles_for_month(self, client, requests_mock, top_articles):
        """Tests the happy path for top articles for month"""
        requests_mock.get(mocks.ANY, json=top_articles)
        response = client.get(top_articles_for_month_base_url + '2023/1')
        articles = response.json['articles']
        assert len(articles) == 3
        assert articles[0] == {'article': 'Main_Page', 'rank': 1, 'views': 100}
        assert articles[1] == {'article': 'Special:Search', 'rank': 2, 'views': 10}

    def test_top_articles_for_week(self, client, requests_mock, top_articles):
        """Tests the happy path for top articles for week"""
        requests_mock.get(mocks.ANY, json=top_articles)
        response = client.get(top_articles_for_week_base_url + '2023/1')
        articles = response.json['articles']
        assert len(articles) == 3
        assert articles[0] == {'article': 'Main_Page', 'rank': 1, 'views': 700}
        assert articles[1] == {'article': 'Special:Search', 'rank': 2, 'views': 70}
