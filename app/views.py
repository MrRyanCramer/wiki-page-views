from flask import Blueprint, abort
import requests
from markupsafe import escape
import datetime
from app.wikipedia_service import WikipediaService

from functools import reduce

bp = Blueprint("views", __name__, url_prefix="/views")


@bp.route("/hello")
def hello_world():
    return "Hello, World!"


@bp.route("/hello/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


@bp.route('/test')
def test():
    url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/2023/11/01'
    headers = {'User-Agent': 'grow-therapy-take-home/0.0.1',
               "accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

@bp.route('/article/week/<article>/<int:year>/<int:week>')
def views_for_article_in_week(article: str, year: int, week: int):
    # Route example 127.0.0.1:5000/views/article/week/Dawngate/2023/1

    service = WikipediaService()
    view_data = service.get_weekly_views_for_article(article, year, week)

    days = view_data['items']
    views_in_week = reduce(lambda view_total, day: view_total + day['views'], days, 0)
    return {'views': views_in_week}

@bp.route('/top-day/<article>/<int:year>/<int:month>')
def top_day_for_article_in_month(article: str, year: int, month: int):
    # Route example 127.0.0.1:5000/views/top-day/Dawngate/2023/11
    # Validate input

    # Build and fire request
    service = WikipediaService()
    view_data = service.get_daily_views_for_article(article, year, month)

    # Find day with most views
    days = view_data['items']
    max_timestamp = max(days, key=lambda day: day['views'])['timestamp']
    formatted_day = datetime.datetime.strptime(max_timestamp, '%Y%m%d%H').day
    return {'day': formatted_day}

