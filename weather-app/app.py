from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
API_KEY = "6fdb18a3c9bd0bae7d0a2a947f0fae13"
BASE_URL = "https://api.openweathermap.org/data/2.5"

# Helper: fetch JSON from OpenWeatherMap
def fetch(url, params):
    params['appid'] = API_KEY
    return requests.get(url, params=params).json()

@app.route('/', methods=['GET', 'POST'])
def index():
    city = request.form.get('city', 'Kathmandu')  # default
    return render_template('index.html', city=city)

@app.route('/api/weather')
def weather_api():
    city = request.args.get('city', 'Kathmandu')
    # 1. Get lat/lon
    geocode = fetch(f"{BASE_URL}/weather", { 'q': city + ',NP', 'units': 'metric' })
    lat, lon = geocode['coord']['lat'], geocode['coord']['lon']
    # 2. Current + forecast
    onecall = fetch(f"{BASE_URL}/onecall", {
        'lat': lat, 'lon': lon,
        'units': 'metric', 'exclude': 'minutely,alerts',
        'aqi': 'yes'
    })
    # 3. Historical: last 3 days
    hist = []
    for days in range(1, 4):
        dt = int((datetime.utcnow() - timedelta(days=days)).timestamp())
        h = fetch(f"{BASE_URL}/onecall/timemachine", {
            'lat': lat, 'lon': lon, 'dt': dt, 'units': 'metric'
        })
        hist.append({ 'dt': dt, 'data': h['current'] })

    return jsonify({
        'current': onecall['current'],
        'daily': onecall['daily'],
        'hourly': onecall['hourly'],
        'air_quality': onecall.get('aqi'),
        'historical': hist
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
