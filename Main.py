import os
from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect
from functions import Functions
from validators import RegistrationForm, LoginForm
from weather_app import WeatherApp
import secrets

# Master *****************************************************************************************************
app = Flask(__name__)
weather_app_object = WeatherApp()
functions = Functions()
is_first_log = True
# Get it like : secrets.token_hex(16)
app.config.update({"SECRET_KEY":"a458918b381a3ee2a83cebfca2320ac0"})

# Routes *****************************************************************************************************
@app.route("/")
def index():
    return render_template("index.html", title = "Home")

@app.route("/weather-app", methods = ["GET", "POST"])
def weather_app():
    if request.method == "POST":
        weather_app_object.city_name = request.form.get("city-input").lower()
        weather_app_object.get_weather()
        #print(f"def weather_app - weather_app_object.data : {weather_app_object.data}")
        if weather_app_object.data:
            return render_template("weather-app.html", title = "Weather app by Peter Szepesi",
                                   data = weather_app_object.data, local_time = weather_app_object.local_time,
                                   misc_data = weather_app_object.misc_data,
                                   astro_data=weather_app_object.astro_data,
                                   uv_index = weather_app_object.uv_index,
                                   uv_desc = weather_app_object.uv_description,
                                   weather_icon = weather_app_object.weather_icon_path,
                                   temperature = weather_app_object.temperature,
                                   temp_sign = weather_app_object.temp_sign,
                                   wind_symbol = weather_app_object.wind_symbol,
                                   wind_speed=weather_app_object.wind_speed,
                                   speed_unit = weather_app_object.speed_unit,
                                   active_tab = "current", geo_data = weather_app_object.geo_data,
                                   sunrise = weather_app_object.sunrise, sunset = weather_app_object.sunset)
        else:
            return redirect("/weather-app")

    return render_template("weather-app.html", title = "Weather app by Peter Szepesi",
                           data = weather_app_object.data, local_time = weather_app_object.local_time,
                           misc_data=weather_app_object.misc_data,
                           astro_data=weather_app_object.astro_data,
                           uv_index=weather_app_object.uv_index,
                           uv_desc=weather_app_object.uv_description,
                           weather_icon = weather_app_object.weather_icon_path,
                           temperature = weather_app_object.temperature,
                           temp_sign = weather_app_object.temp_sign,
                           wind_symbol = weather_app_object.wind_symbol,
                           wind_speed = weather_app_object.wind_speed,
                           speed_unit = weather_app_object.speed_unit,
                           active_tab = "current", geo_data = weather_app_object.geo_data,
                           sunrise = weather_app_object.sunrise, sunset = weather_app_object.sunset)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if request.method == "POST":
        print(f"def register : test")

    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        print(f"def login : test")
    return render_template("login.html", title="Login", form=form)

# Main *******************************************************************************************************
if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        functions.write_log("******************************* Initial run *******************************************")
        is_first_log = False

    app.run(host = "0.0.0.0", debug=True)