import datetime

import requests
from functions import Functions


class WeatherApp:
    def __init__(self):
        self.api_key = "f0130aa9896b42e7eec767c74fbb474b"
        self.city_name = "Hrhov"
        self.functions = Functions()
        self.data = None
        self.local_time = None
        self.weather_icon_path = "Images/sun - minimalist.png"

    def get_weather(self):

        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city_name}&appid={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                self.data = response.json()
                self.format_data()
        except Exception as e:
            self.functions.write_log(f"def get_weather : {e}")
            self.data = None

    def format_data(self):

        # Formatting time
        unix_timestamp = int(self.data.get("dt"))
        time_zone_correction = int(self.data.get("timezone"))
        utc_time = datetime.datetime.fromtimestamp(unix_timestamp, datetime.UTC)
        local_time_temp = utc_time + datetime.timedelta(seconds=time_zone_correction)
        self.local_time = local_time_temp.strftime("%d.%m.%Y %H:%M:%S")

        # Getting the icon
        if 200 <= self.weather_code <= 232:
            self.weather_icon_path = "Images/thunderstorm - minimalist.png"
        elif 300 <= self.weather_code <= 321:
            self.weather_icon_path = "Images/rain - minimalist.png"
        elif 500 <= self.weather_code <= 504:
            self.weather_icon_path = "Images/rain - minimalist.png"
        elif self.weather_code == 511:
            self.weather_icon_path = "Images/snowfall - minimalist.png"
        elif 520 <= self.weather_code <= 522 or self.weather_code == 531:
            self.weather_icon_path = "Images/rain - minimalist.png"
        elif 600 <= self.weather_code <= 622:
            self.weather_icon_path = "Images/snowfall - minimalist.png"
        elif 701 <= self.weather_code <= 781:
            self.weather_icon_path = "Images/fog - minimalist.png"
        elif self.weather_code == 800:
            self.weather_icon_path = "Images/sun - minimalist.png"
        elif 801 <= self.weather_code <= 804:
            self.weather_icon_path = "Images/cloud - minimalist.png"