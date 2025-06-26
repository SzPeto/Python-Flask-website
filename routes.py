from flask import Flask, render_template, url_for, request, flash, get_flashed_messages
from werkzeug.utils import redirect
from validators import RegistrationForm, LoginForm

from Main import app, db, weather_app_object, functions
from db_models import User, Post


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
        if form.validate_on_submit():
            flash(f"Account successfully created : {form.email_username.data}", "success")
            email_username = request.form.get("email_username")
            password = request.form.get("password")
            entry = User(email_username=email_username, password=password)
            db.session.add(entry)
            db.session.commit()
        else:
            if form.email_username.errors:
                for error in form.email_username.errors:
                    flash(f"Email - username : {error}", "warning")
            if form.password.errors:
                for error in form.password.errors:
                    flash(f"Password : {error}", "warning")
            if form.confirm_password.errors:
                for error in form.confirm_password.errors:
                    flash(f"Confirm password : {error}", "warning")

    # For debugging purposes only
    entries = User.query.all()
    for i in range(0, len(entries)):
        print(entries[i]) # Since we have defined __repr__ of class, we can print the string representation of object
        for j in range(0, len(entries[i].posts)):
            print(entries[i].posts[j])

    # Rendering the page
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            flash(f"Login successful! {form.email_username.data}", "success")
        else:
            if form.email_username.errors:
                for error in form.email_username.errors:
                    flash(f"Email - username : {error}", "warning")
            if form.password.errors:
                for error in form.password.errors:
                    flash(f"Password : {error}", "warning")

    return render_template("login.html", title="Login", form=form)

@app.route("/blog", methods=["GET", "POST"])
def blog():
    # Dummy post
    Post.query.delete()
    entry = Post(title="Title 1", content="This is a test post to test the functionality", user_id=1)
    db.session.add(entry)
    db.session.commit()

    # Getting all posts
    posts = Post.query.all()
    return render_template("blog.html", title="Blog", posts=posts)