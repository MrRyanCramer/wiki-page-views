import datetime
import urllib.parse

import requests
from requests import Response
import app.date_util as date_util
from enum import Enum


def _format_article(article: str) -> str:
    return urllib.parse.quote(article)


class Granularity(Enum):
    daily = 'daily'
    monthly = 'monthly'


class WikipediaService:

    _views_per_article_base_url: str = \
        'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/'
    _top_viewed_articles_base_url = \
        'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/'
    _headers = {'User-Agent': 'grow-therapy-take-home/0.0.1',
                "accept": "application/json"}
    granularity = {}

    def get_top_articles_for_week(self, year: int, week: int):
        # Validate input
        last_day_in_week = date_util.get_week_range(year, week)[1]
        date_util.verify_date_in_past(last_day_in_week)

        # Build a dictionary of article_title to article_views
        view_data = {}
        # For each day in the range, get the top 1000 articles
        days = date_util.get_dates_for_week(year, week)
        for day in days:
            url = self._build_daily_top_url(day)
            response = self._send_request(url)
            articles = response.json()['items'][0]['articles']
            # Populate the map, adding the day's views for every article in the top 1000 of the day
            for article in articles:
                title = article['article']
                view_data[title] = view_data.get(title, 0) + article['views']
        # Now that the map is populated, sort it to find the highest view articles
        sorted_articles = sorted(view_data.items(), key=lambda item: item[1], reverse=True)
        # Only return the top 1000 articles
        filtered_articles = sorted_articles[0:1000]
        # Format the output
        formatted_articles = [{'article': article[0],
                               'views': article[1],
                               'rank': rank + 1} for rank, article in enumerate(filtered_articles)]
        return formatted_articles

    def get_top_articles_for_month(self, year: int, month: int):
        # Validate input
        last_day_of_month = date_util.get_month_range(year, month)[1]
        date_util.verify_date_in_past(last_day_of_month)

        # Build and send request
        url = self._build_monthly_top_url(last_day_of_month)
        response = self._send_request(url)

        # Format response
        return response.json()['items'][0]['articles']

    def get_daily_views_for_article(self, article: str, year: int, month: int):
        """Returns a list of daily view information for each day in the given month for the given article

        Each entry in the list represents a day with a 'timestamp' and 'views' property.
        """
        # Validate input
        first_day_of_month, last_day_of_month = date_util.get_month_range(year, month)
        date_util.verify_date_in_past(last_day_of_month)
        formatted_article = _format_article(article)

        # Build and send request
        url = self._build_views_per_article_url(formatted_article, first_day_of_month, last_day_of_month, Granularity.daily)
        response = self._send_request(url)

        # Format response
        return response.json()['items']

    def get_weekly_views_for_article(self, article: str, year: int, week: int):

        # Validate input
        first_day_in_week, last_day_in_week = date_util.get_week_range(year, week)
        date_util.verify_date_in_past(last_day_in_week)
        formatted_article = _format_article(article)

        # Build and send request
        url = self._build_views_per_article_url(formatted_article, first_day_in_week, last_day_in_week, Granularity.daily)
        response = self._send_request(url)

        # Format response
        return response.json()['items']

    def get_monthly_views_for_article(self, article: str, year: int, month: int):

        # Validate input
        first_day_in_month, last_day_in_month = date_util.get_month_range(year, month)
        date_util.verify_date_in_past(last_day_in_month)
        formatted_article = _format_article(article)

        # Build and send request
        url = self._build_views_per_article_url(formatted_article, first_day_in_month, last_day_in_month, Granularity.monthly)
        response = self._send_request(url)

        # Format response
        return response.json()['items'][0]

    def _build_views_per_article_url(self, article: str, start_date: datetime.date, end_date: datetime.date, granularity: Granularity):
        formatted_start = start_date.strftime("%Y%m%d")
        formatted_end = end_date.strftime("%Y%m%d")
        return self._views_per_article_base_url + article + '/' + granularity.value + '/' + formatted_start + '/' + formatted_end

    def _build_monthly_top_url(self, date: datetime.date) -> str:
        return self._top_viewed_articles_base_url + date.strftime('%Y/%m/all-days')

    def _build_daily_top_url(self, date: datetime.date) -> str:
        return self._top_viewed_articles_base_url + date.strftime('%Y/%m/%d')

    def _send_request(self, url: str) -> Response:
        response = requests.get(url, headers=self._headers)
        response.raise_for_status()
        return response
