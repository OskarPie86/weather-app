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


from bson import ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
CORS(app)

client = MongoClient("mongodb://localhost:27017")
db = client['tenerife']
weather_collection = db['weather']

def save_to_mongodb(x):
    current_weather = {
        "area" : x["name"],
        "temp" : convert_C(x["main"]["temp"]),
        "temp_min" : convert_C(x["main"]["temp_min"]),
        "temp_max" : convert_C(x["main"]["temp_max"]),
        "humidity" : x["main"]["humidity"],
        "pressure" : x["main"]["pressure"],
        "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "desc": f"{x['weather'][0]['main']}, {x['weather'][0]['description']}"
    }
    
    weather_collection.insert_one(current_weather)
    
last_city=None
    
def job():
    global last_city
    data = get_weather(last_city)
    if data:
        save_to_mongodb(data)
        print("Dostarczono nowe dane")
    else:
        print("Nie udało się pobrać danych")


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'interval', seconds=10)
scheduler.start()

@app.route('/', methods=['GET', 'POST'])
def weather():
    global last_city

    if request.method == 'POST':
        last_city = request.form['city']
        if last_city:
            weather_data = get_weather(last_city)
            return render_template('weather_search.html', city=city, weather_data=weather_data)
        
    return render_template('weather_search.html', city=last_city, weather_weather_data=None)


@app.route("/chart")
def generate_chart():
    chart_data = weather_collection.find({},{'_id':0, 'temp':1,'timestamp':1}).sort([('_id',-1)]).limit(10)
    data = list(chart_data)
    timestamps =[datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S").hour for entry in data]
    temperatures = [entry['temp'] for entry in data]
    print(timestamps)
    print(temperatures)
    
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    axis.bar(timestamps, temperatures)
    axis.set_xlabel("Time")
    axis.set_ylabel("Temperature")
    axis.set_title("Tenerife weather")
    
    canvas = FigureCanvasAgg(fig)
    png = io.BytesIO()
    canvas.print_png(png)
    
    # wyświetlenie wykresu na stronie
    return  png.getvalue(), 200, {"Content-Type":"image/png"}
