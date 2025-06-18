from flask import Flask, render_template, url_for, request

from functions import Functions
from weather_app import WeatherApp

# Master *****************************************************************************************************
app = Flask(__name__)
weather_app = WeatherApp()
functions = Functions()
weather_app.get_weather()

# Routes *****************************************************************************************************
@app.route("/")
def index():
    return render_template("index.html", title = "Home")

@app.route("/weather-app", methods = ["GET", "POST"])
def weather_app():

    if request.method == "POST":
        city = request.form.get("city-input")
        print(city)

    return render_template("weather-app.html", title = "Weather app by Peter Szepesi")

# Main *******************************************************************************************************
if __name__ == "__main__":
    app.run(debug = True)