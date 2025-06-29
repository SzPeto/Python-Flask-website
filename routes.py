from flask import render_template, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import redirect
from validators import RegistrationForm, LoginForm, UpdateForm

from Main import app, db, weather_app_object, functions, bcrypt
from db_models import User, Post

@app.route("/")
def index():
    return render_template("index.html", title = "Home", current_user=current_user)

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
                                   sunrise = weather_app_object.sunrise, sunset = weather_app_object.sunset,
                                   current_user=current_user)
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
                           sunrise = weather_app_object.sunrise, sunset = weather_app_object.sunset,
                           current_user=current_user)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email_username = form.email_username.data
            password = form.password.data
            encrypted_pw = bcrypt.generate_password_hash(password).decode("utf-8")
            entry = User(email_username=email_username, password=encrypted_pw)
            db.session.add(entry)
            db.session.commit()
            flash(f"Account successfully created : {form.email_username.data}, now you can log in",
                  "success")
            return redirect(url_for("login"))
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
    return render_template("register.html", title="Register", form=form,
                           current_user=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Getting the user based on entered email_username
            user = User.query.filter_by(email_username=form.email_username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    flash(f"Login successful! {form.email_username.data}", "success")
                    return redirect(url_for("index"))
                else:
                    flash("Invalid password!", "warning")
            else:
                flash(f"{form.email_username.data} : account doesn't exist!", "warning")

        else:
            if form.email_username.errors:
                for error in form.email_username.errors:
                    flash(f"Email - username : {error}", "warning")
            if form.password.errors:
                for error in form.password.errors:
                    flash(f"Password : {error}", "warning")

    return render_template("login.html", title="Login", form=form,
                           current_user=current_user)

@app.route("/blog", methods=["GET", "POST"])
def blog():
    # Getting all posts
    posts = Post.query.all()
    return render_template("blog.html", title="Blog", posts=posts,
                           current_user=current_user)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!", "success")
    return redirect(url_for("login"))

@app.route("/user", methods=["GET", "POST"])
@login_required # It means we can access this route only if a user is logged in
def user():
    form = UpdateForm()
    if request.method == "POST":
        if form.validate_on_submit():
            current_user.email_username = form.email_username.data
            print(f"{form.picture_file.data}")
            db.session.commit()
            flash("Account successfully updated!", "success")
        else:
            if form.email_username.errors:
                for error in form.email_username.errors:
                    flash(f"Email - username : {error}", "warning")
            if form.picture_file.errors:
                for error in form.picture_file.errors:
                    flash(f"Profile picture : {error}", "warning")

    # Setting the value of input field to be the current_user.email_username
    form.email_username.data = current_user.email_username
    return render_template("user.html", title="User account", current_user=current_user,
                           form=form)