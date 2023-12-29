import datetime
from requests.exceptions import HTTPError
from functools import reduce

from flask import abort

from .wikipedia_service import WikipediaService
from . import api
from ..exceptions import ValidationError


@api.route('/top-articles/week/<int:year>/<int:week>')
def top_articles_for_week(year: int, week: int):
    service = WikipediaService()
    articles = service.get_top_articles_for_week(year, week)
    # TODO Consider better formatting for output instead of tuples
    return {'articles': articles}


@api.route('/top-articles/month/<int:year>/<int:month>')
def top_articles_for_month(year: int, month: int):
    # Fetch view information from service
    articles = WikipediaService().get_top_articles_for_month(year, month)
    return {'articles': articles}


@api.route('/article/week/<article>/<int:year>/<int:week>')
def views_for_article_in_week(article: str, year: int, week: int):
    # Fetch view information from service
    days = WikipediaService().get_weekly_views_for_article(article, year, week)
    # Aggregate view information for the week
    views_in_week = reduce(lambda view_total, day: view_total + day['views'], days, 0)
    return {'views': views_in_week}


@api.route('/article/month/<article>/<int:year>/<int:month>')
def views_for_article_in_month(article: str, year: int, month: int):
    """Returns the view count of a specific article for a given month"""
    # Fetch view information from service
    view_data_for_month = WikipediaService().get_monthly_views_for_article(article, year, month)
    views = view_data_for_month['views']
    return {'views': views}


@api.route('/top-day/<article>/<int:year>/<int:month>')
def top_day_for_article_in_month(article: str, year: int, month: int):
    """Returns the day of the month when an article got the most page views."""
    # Fetch view information from service
    days = WikipediaService().get_daily_views_for_article(article, year, month)
    # Find day with most views
    max_timestamp = max(days, key=lambda day: day['views'])['timestamp']
    # Format value for return
    formatted_day = datetime.datetime.strptime(max_timestamp, '%Y%m%d%H').day
    return {'day': formatted_day}
