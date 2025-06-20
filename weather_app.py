import datetime

import requests
from functions import Functions


class WeatherApp:
    def __init__(self):
        self.api_key = "f0130aa9896b42e7eec767c74fbb474b"
        self.city_name = "Hrhov"
        self.functions = Functions()
        self.geo_data = None
        self.data = None
        self.local_time = None
        self.weather_icon_path = None
        self.weather_code = None
        self.temperature = "0.00"
        self.temp_unit = "c"
        self.temp_sign = "°C"
        self.speed_unit = "km/h"
        self.wind_symbol = "⬆️"
        self.wind_speed = 0.0
        self.sunrise = None
        self.sunset = None

    def get_weather(self):
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={self.city_name}&limit=1&appid={self.api_key}"
        try:
            geo_response = requests.get(geo_url)
            geo_response.raise_for_status()
            if geo_response.status_code == 200:
                self.geo_data = geo_response.json()
                lat = self.geo_data[0].get("lat")
                lon = self.geo_data[0].get("lon")
                print(self.geo_data)
                url_new = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}"
        except Exception as e:
            self.functions.write_log(f"def get_weather - geo_response : {e}")

        try:
            if url_new:
                response = requests.get(url_new)
                response.raise_for_status()
                if response.status_code == 200:
                    self.data = response.json()
                    print(self.data)
                    self.format_data()
        except Exception as e:
            self.functions.write_log(f"def get_weather response : {e}")
            self.data = None

    def format_data(self):

        # Formatting time
        self.local_time = self.calculate_local_time(int(self.data.get("dt")))
            # Sunrise
        self.sunrise = self.calculate_local_time(int(self.data.get("sys").get("sunrise")), with_date=False)
            # Sunset
        self.sunset = self.calculate_local_time(int(self.data.get("sys").get("sunset")), with_date=False)
        print(f"{self.local_time}, {self.sunrise}, {self.sunset}")

        # Formatting temperature
        temp_temperature = self.data.get("main").get("temp")
        if self.temp_unit == "c":
            self.temperature = f"{float(temp_temperature - 273.15 + 2):.1f}"
            self.temp_sign = "°C"

        # Getting the icon
        self.weather_code = self.data.get("weather")[0].get("id")
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

        # Setting the wind
        self.set_wind()

    def set_wind(self):
        wind_degree = int(self.data.get("wind").get("deg"))
        wind_symbols = ("⬇️", "↙️", "⬅️", "↖️", "⬆️", "↗️", "➡️", "↘️")
        wind_index = ((wind_degree + 22) % 360) // 45
        self.wind_symbol = wind_symbols[wind_index]
        temp_speed = float(self.data.get("wind").get("speed"))
        if self.speed_unit == "km/h":
            self.wind_speed = int(temp_speed * 3.6)

    def calculate_local_time(self, unix_timestamp, with_date=True):
        time_zone_correction = int(self.data.get("timezone"))
        utc_time = datetime.datetime.fromtimestamp(unix_timestamp, datetime.UTC)
        temp_time = utc_time + datetime.timedelta(seconds=time_zone_correction)
        if with_date:
            return temp_time.strftime("%d.%m.%Y %H:%M:%S")
        return temp_time.strftime("%H:%M:%S")