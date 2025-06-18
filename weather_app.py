import requests
from functions import Functions


class WeatherApp:
    def __init__(self):
        self.api_key = "f0130aa9896b42e7eec767c74fbb474b"
        self.city_name = "Hrhov"
        self.functions = Functions()

    def get_weather(self):

        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city_name}&appid={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                print(data)
        except Exception as e:
            self.functions.write_log(f"def get_weather : {e}")
