# import requests
# # pobiranie danych pogodowych


# def get_weather():
#     API_KEY = "dd7f46c97a7dd8e7801668d57cd76a05"
#     CITY = "Tenerife"
    
#     URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
    
#     response = requests.get(URL)
#     return response.json()

# from flask import Flask, render_template, request
# import requests
# import json

# app = Flask(__name__)

# # Klucz API OpenWeatherMap
# API_KEY = "dd7f46c97a7dd8e7801668d57cd76a05"

# @app.route('/', methods=['GET', 'POST'])
# def weather():
#     city = ''
#     weather_data = None

#     if request.method == 'POST':
#         city = request.form['city']
#         if city:
#             weather_data = get_weather_data(city)

#     return render_template('weather.html', city=city, weather_data=weather_data)

# def get_weather(city):
#     try:
#         # Tworzymy zapytanie do API OpenWeatherMap
#         url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
#         response = requests.get(url)
#         data = json.loads(response.text)

#         if data['cod'] == 200:
#             weather_info = {
#                 'city': data['name'],
#                 'temperature': data['main']['temp'],
#                 'description': data['weather'][0]['description'],
#             }
#             return weather_info
#         else:
#             return None
#     except Exception as e:
#         print(f"Error: {e}")
#         return None

# if __name__ == '__main__':
#     app.run(debug=True)

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
        data = json.loads(response.text)

        if data['cod'] == 200:
            weather_info = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
            }
            return weather_info
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)