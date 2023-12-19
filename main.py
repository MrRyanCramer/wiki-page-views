from flask import Flask
import requests
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<name>")
def hello(name):
    return f"<p>Hello, {escape(name)}!"


@app.route('/test')
def test():
    url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/2023/11/01'
    headers = {'User-Agent': 'grow-therapy-take-home/0.0.1',
               "accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data
