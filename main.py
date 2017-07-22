import datetime
import json

import requests
from flask import Flask, render_template
from flask_bower import Bower

url = "http://transport.opendata.ch/v1/connections"
_BASE = 'Bern'

app = Flask(__name__)
Bower(app)


def _from(location):
    """Get the connections in the morning"""
    c = get_connections(location, _BASE, '07:00')

    return render(c)


def to(location):
    """Get the connections in the evening"""
    c = get_connections(_BASE, location, '17:00')

    return render(c)


def late(location):
    c = get_connections(_BASE, location, '23:00')

    return render(c)


def get_connections(_from, to, time):
    today = datetime.date.today()
    diff = datetime.timedelta(days=today.weekday())
    date = today - diff
    data = {
        'from': _from,
        'to': to,
        'time': time,
        'limit': 6,
        'date': date
    }
    r = requests.get(url, data)
    data = r.json()

    return data['connections']


def get_time(time_str):
    # 2017-07-22T07:09:00+0200
    format = "%Y-%m-%dT%H:%M:%S%z"
    date = datetime.datetime.strptime(time_str, format)

    return (date.strftime('%Y-%m-%d'),
            date.strftime('%H:%M'))


def render_duration(duration):
    days, hours = duration.split('d')

    return hours


def render_one(data):
    products = data['products']
    transfers = data['transfers']
    duration = data['duration']

    date, time = get_time(data['from']['departure'])

    return {
        'products': ','.join(products),
        'transfers': transfers,
        'duration': render_duration(duration),
        'date': date,
        'time': time
    }


def render(data):
    return [render_one(c) for c in data]


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/data/<string:location>')
def data(location):
    return json.dumps({
        'from': _from(location),
        'to': to(location),
        'late': late(location)
    })
