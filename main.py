from flask import Flask, render_template, request, redirect, url_for, jsonify
from utils.fetch_weather_data import get_weather
from pymongo import MongoClient
from datetime import datetime
from utils.conv_temp import convert_C
from apscheduler.schedulers.background import BackgroundScheduler

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
import requests
import json
import base64


from bson import ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
CORS(app)

client = MongoClient("mongodb://localhost:27017")
db = client['City_weather']
weather_collection = db['weather']

scheduler = BackgroundScheduler()
scheduler.start()

last_city=None

def save_to_mongodb(x):
    current_weather = {
        "area" : x['city'],
        "temp" : x["temperature"]["temp"],
        "temp_min" : x["temperature"]["temp_min"],
        "temp_max" : x["temperature"]["temp_max"],
        "humidity" : x["temperature"]["humidity"],
        "pressure" : x["temperature"]["pressure"],
        "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "desc": f"{x['description']}"
    }
    
    weather_collection.insert_one(current_weather)
    
def job():
    global last_city
    if last_city:
        data = get_weather(last_city)
        if data:
            print(data)  # Dodaj ten print, aby zobaczyć, co jest zawarte w 'data'
            save_to_mongodb(data)
            print("Dostarczono nowe dane")
        else:
            print("Nie udało się pobrać danych")

scheduler.add_job(job, 'interval', seconds=10)

@app.route('/', methods=['GET', 'POST'])
def index():
    global last_city
    latest_data = []

    if request.method == 'POST':
        last_city = request.form.get('city')
        if last_city:

            latest_data = weather_collection.find().sort([('_id',-1)]).limit(30)
    return render_template("index.html", weather_data=list(latest_data))


@app.route('/base')
def base():
    city = request.args.get('city')
    weather_data = weather_collection.find_one({"_id": city})
    return render_template('base.html', city=city, weather_data=weather_data)

@app.route('/weather_search', methods=['POST'])
def weather():
    global last_city
    last_city = request.form.get('city')
    return render_template('index.html', city=last_city)

@app.route('/chart')
def chart():
    chart_data = weather_collection.find({}, {'_id': 0, 'temp': 1, 'timestamp': 1}).sort([('_id', -1)]).limit(10)
    data = list(chart_data)
    timestamps = [entry['timestamp'] for entry in data]
    temperatures = [entry['temp'] for entry in data]

    fig = Figure(figsize=(12,10)) 
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(timestamps, temperatures)
    axis.set_xlabel("Timestamp")
    axis.set_ylabel("Temperatures (°C)")
    axis.set_title("Temperatures Chart")
    num_labels = 5  # Liczba etykiet, które chcesz wyświetlić
    step = len(timestamps) // num_labels
    axis.set_xticks(range(0, len(timestamps), step))
    axis.set_xticklabels(timestamps[::step], rotation=45)
    for label in axis.get_xticklabels():
        label.set_size(6)
    
    canvas = FigureCanvasAgg(fig)
    png = io.BytesIO()
    canvas.print_png(png)
    plot_url = "data:image/png;base64," + base64.b64encode(png.getvalue()).decode('utf-8')
    
    return render_template('chart.html', plot_url=plot_url, city=last_city)



