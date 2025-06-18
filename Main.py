import os

from flask import Flask, render_template, url_for, request

from functions import Functions
from weather_app import WeatherApp

# Master *****************************************************************************************************
app = Flask(__name__)
weather_app_object = WeatherApp()
functions = Functions()
is_first_log = True

# Routes *****************************************************************************************************
@app.route("/")
def index():
    return render_template("index.html", title = "Home")

@app.route("/weather-app", methods = ["GET", "POST"])
def weather_app():
    if request.method == "POST":
        weather_app_object.city_name = request.form.get("city-input").lower()
        weather_app_object.get_weather()
        return render_template("weather-app.html", title="Weather app by Peter Szepesi",
                               data = weather_app_object.data)

    return render_template("weather-app.html", title = "Weather app by Peter Szepesi",
                           data = {})

# Main *******************************************************************************************************
if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        functions.write_log("******************************* Initial run *******************************************")
        is_first_log = False

    app.run(debug = True)