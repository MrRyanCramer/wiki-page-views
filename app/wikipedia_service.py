import requests
from requests import Response

from app.date import get_datetime_range_for_month, get_datetime_range_for_week


class WikipediaService:
    _views_per_article_base_url: str = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/'
    _headers = {'User-Agent': 'grow-therapy-take-home/0.0.1',
                "accept": "application/json"}

    def _build_daily_url(self, article: str, year: int, month: int) -> str:
        formatted_start, formatted_end = get_datetime_range_for_month(year, month)
        return self._views_per_article_base_url + article + '/daily/' + formatted_start + '/' + formatted_end

    def _build_weekly_url(self, article: str, year: int, week: int) -> str:
        formatted_start, formatted_end = get_datetime_range_for_week(year, week)
        return self._views_per_article_base_url + article + '/daily/' + formatted_start + '/' + formatted_end

    def get_daily_views_for_article(self, article: str, year: int, month: int):
        url = self._build_daily_url(article, year, month)
        response = self._send_request(url)
        return response.json()
        # Verify response
        # if response.status_code != requests.codes.ok:
        #     abort(404)
        #
        # # JSONDecodeError possible here
        # data = response.json()
        # if 'items' not in data:
        #     abort(404)

    def get_weekly_views_for_article(self, article: str, year: int, week: int):
        url = self._build_weekly_url(article, year, week)
        response = self._send_request(url)
        return response.json()

    def _send_request(self, url: str) -> Response:
        return requests.get(url, headers=self._headers)
