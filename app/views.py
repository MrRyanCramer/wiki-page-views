from flask import Blueprint, abort
import requests
from markupsafe import escape
import datetime
import calendar

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


@bp.route('/article/month/<article>/<int:year>/<int:month>')
def top_viewed_articles_by_month(article: str, year: int, month: int):
    # Route example 127.0.0.1:5000/views/article/month/Dawngate/2023/11
    # Validate input

    # Format input
    last_day = calendar.monthrange(year, month)[1]
    begin_date = datetime.datetime(year, month, 1)
    end_date = datetime.datetime(year, month, last_day)
    formatted_begin = begin_date.strftime("%Y%m%d%H")
    formatted_end = end_date.strftime("%Y%m%d%H")

    # Build and fire request
    base_url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/'
    url = base_url + article + '/daily/' + formatted_begin + '/' + formatted_end
    headers = {'User-Agent': 'grow-therapy-take-home/0.0.1',
               "accept": "application/json"}
    response = requests.get(url, headers=headers)

    # Verify response
    if response.status_code != requests.codes.ok:
        abort(404)

    # JSONDecodeError possible here
    data = response.json()
    if 'items' not in data:
        abort(404)


    # Find day with most views
    days = data['items']
    max_timestamp = max(days, key=lambda day: day['views'])['timestamp']
    formatted_day = datetime.datetime.strptime(max_timestamp, '%Y%m%d%H').day
    return {'day': formatted_day}
