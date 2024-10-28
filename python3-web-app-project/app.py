from flask import Flask, render_template, redirect, request, url_for
from geopy.geocoders import Nominatim
from flask import send_file
from datetime import datetime
import requests
import os
import json
from dayClass import Day


app = Flask(__name__)

@app.route('/')
def home():
    bg_color = os.getenv('BG_COLOR', 'white')
    return render_template("index.html", bg_color=bg_color)

@app.route('/', methods=['POST'])
def home_post():
    name = request.form['location']
    return redirect(url_for('location', name=name))

@app.route('/locations/<name>')
def location(name):
    geolocator = Nominatim(user_agent='weather')
    loc = geolocator.geocode(name, language="en")
    try:
        lat = loc.latitude
        lon = loc.longitude

    except Exception:
        return {'error':'wrong input'}

    quary = 'hourly=temperature_2m,relative_humidity_2m'
    url = 'https://api.open-meteo.com/v1/forecast'

    try:
        response = requests.get('{}?latitude={}&longitude={}&{}'.format(url, lat, lon, quary))
    except requests.exceptions.RequestException as e:
        return {'error':'something wrong happend'}

    hourly = response.json().get('hourly')
    days = []
    for i in range(11,len(hourly.get('time')), 24):
        date = hourly.get('time')[i][:10]
        day_temperature = hourly.get('temperature_2m')[i]
        night_temperature = hourly.get('temperature_2m')[i+12]
        humidity = hourly.get('relative_humidity_2m')[i]
        day = Day(date, day_temperature, night_temperature, humidity)
        days.append(day)
    date_str = datetime.now().strftime("%Y-%m-%d")
    days_json = []
    for day in days:
        day_data = {
            'date': day.get_date(),
            'day_temperature': day.get_day_temperature(),
            'night_temperature': day.get_night_temperature(),
            'humidity': day.get_humidity()
        }
        days_json.append(day_data)

    history = {
        'date': date_str,
        'location': name,
        'days': days_json
    }

    file_name = 'h_'+name+'_'+date_str+'.json'
    with open(file_name, 'w') as f:
        json.dump(history, f, indent=4)

    loc_arr = loc.address.split(',')
    return render_template("location.html", days=days, name=loc_arr[0]+', '+loc_arr[-1])


@app.route('/history')
def history():
    history_files = [f for f in os.listdir('.') if f.startswith('h_') and f.endswith('.json')]
    return render_template("history.html", history_files=history_files)


@app.route('/download-history/<filename>')
def download_history(filename):
    return send_file(filename, as_attachment=True)

@app.errorhandler(404)
def error_404(e):
  return "<h1>Page not found</h1>"

if __name__ == '__main__':
    app.run(debug=False)

