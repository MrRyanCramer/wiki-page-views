import datetime
import urllib.parse

import requests
from flask import abort
from requests import Response
import app.date_util as date_util
from app.exceptions import ValidationError

# from app.date import get_datetime_range_for_month, get_datetime_range_for_week


def _validate_month(year: int, month: int):
    input_date = datetime.date(year, month, 1)
    if input_date > datetime.date.today():
        raise ValidationError("Date information provided must be in the past")


def _validate_article(article: str):
    return urllib.parse.quote(article)


class WikipediaService:

    _views_per_article_base_url: str = \
        'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/'
    _top_viewed_articles_base_url = \
        'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/'
    _headers = {'User-Agent': 'grow-therapy-take-home/0.0.1',
                "accept": "application/json"}

    def get_top_articles_for_week(self, year: int, week: int):
        days = date_util.get_dates_for_week(year, week)
        view_data = {}
        for day in days:
            url = self._build_daily_top_url(day)
            response = self._send_request(url)
            articles = response.json()['items'][0]['articles']
            for article in articles:
                title = article['article']
                view_data[title] = view_data.get(title, 0) + article['views']
        sorted_articles = sorted(view_data.items(), key=lambda item: item[1], reverse=True)
        filtered_articles = sorted_articles[0:1000]
        return filtered_articles

    def get_top_articles_for_month(self, year: int, month: int):
        url = self._build_monthly_top_url(year, month)
        response = self._send_request(url)
        return response.json()

    def get_daily_views_for_article(self, article: str, year: int, month: int):
        _validate_month(year, month)
        article = _validate_article(article)

        url = self._build_daily_views_url(article, year, month)
        response = self._send_request(url)
        if response.status_code != requests.codes.ok:
            abort(404)
        return response.json()

    def get_weekly_views_for_article(self, article: str, year: int, week: int):
        url = self._build_weekly_views_url(article, year, week)
        response = self._send_request(url)
        return response.json()

    def get_monthly_views_for_article(self, article: str, year: int, month: int):
        url = self._build_monthly_views_url(article, year, month)
        response = self._send_request(url)
        return response.json()

    def _build_daily_views_url(self, article: str, year: int, month: int) -> str:
        formatted_start, formatted_end = date_util.get_datetime_range_for_month(year, month)
        return self._views_per_article_base_url + article + '/daily/' + formatted_start + '/' + formatted_end

    def _build_weekly_views_url(self, article: str, year: int, week: int) -> str:
        formatted_start, formatted_end = date_util.get_datetime_range_for_week(year, week)
        return self._views_per_article_base_url + article + '/daily/' + formatted_start + '/' + formatted_end

    def _build_monthly_views_url(self, article: str, year: int, month: int) -> str:
        formatted_start, formatted_end = date_util.get_datetime_range_for_month(year, month)
        return self._views_per_article_base_url + article + '/monthly/' + formatted_start + '/' + formatted_end

    def _build_monthly_top_url(self, year: int, month: int) -> str:
        date = datetime.date.fromisocalendar(year, month, 1)
        return self._top_viewed_articles_base_url + date.strftime('%Y/%m/all-days')

    def _build_daily_top_url(self, date: datetime.date) -> str:
        return self._top_viewed_articles_base_url + date.strftime('%Y/%m/%d')

    def _send_request(self, url: str) -> Response:
        return requests.get(url, headers=self._headers)
