from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Klucz API OpenWeatherMap
API_KEY = "dd7f46c97a7dd8e7801668d57cd76a05"
last_city = None

def get_weather(city):
    try:
        # Tworzymy zapytanie do API OpenWeatherMap
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        print(response.text)
        data = json.loads(response.text)

        if data['cod'] == 200:
            weather_info = {
                'city': data['name'],
                'temperature': data['main'],
                'description': data['weather'][0]['description'],
            }
            return weather_info
        else:
            return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

if __name__ == '__main__':
    app.run(debug=True)