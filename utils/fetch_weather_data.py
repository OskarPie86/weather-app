import requests

# pobiranie danych pogodowych


def get_weather():
    API_KEY = "dd7f46c97a7dd8e7801668d57cd76a05"
    CITY = "Tenerife"
    
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
    
    response = requests.get(URL)
    return response.json()