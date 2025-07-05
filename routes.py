import datetime
import os

from PIL import Image
from flask import render_template, url_for, request, flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import redirect
from validators import RegistrationForm, LoginForm, UpdateForm, PostForm

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
    # get the page number from args - after ? in url, access the multidict value of "page", if no value, default it
    # to 1 and automatically convert the value to int
    page = request.args.get("page", 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)
    return render_template("blog.html", title="Blog", posts=posts,
                           current_user=current_user)

@app.route("/insert-post", methods=["GET", "POST"])
@login_required
def insert_post():
    form = PostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.post_title.data
            content = form.post_content.data
            user_id = current_user.id
            entry = Post(content=content, title=title, user_id=user_id)
            db.session.add(entry)
            db.session.commit()
            flash("Post added", "success")
            return redirect(url_for("blog"))
        else:
            if form.post_title.errors:
                for error in form.post_title.errors:
                    flash(error, "warning")
            if form.post_content.errors:
                for error in form.post_content.errors:
                    flash(error, "warning")

    return render_template("insert-post.html", title="Insert post", current_user=current_user,
                           form=form)

@app.route("/blog/delete-post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    entry = db.session.get(Post, post_id)
    if not entry:
        abort(404)
    if current_user.id != entry.user.id and current_user.id != 1:
        abort(403)
    db.session.delete(entry)
    db.session.commit()
    flash("The post has been successfully deleted!", "success")

    return redirect(url_for("blog"))

@app.route("/blog/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    form = PostForm()
    entry = db.session.get(Post, post_id)
    if not entry:
        abort(404)
    if current_user.id != entry.user_id and current_user.id != 1:
        abort(403)
    if request.method == "POST":
        if form.validate_on_submit():
            entry.title = form.post_title.data
            entry.content = form.post_content.data
            db.session.commit()
            flash("Post successfully updated", "success")
            return redirect(url_for("blog"))
        else:
            if form.post_title.errors:
                for error in form.post_title.errors:
                    flash(error, "warning")
            if form.post_content.errors:
                for error in form.post_content.errors:
                    flash(error, "warning")


    form.post_title.data = entry.title
    form.post_content.data = entry.content

    return render_template("edit-post.html", title="Edit post", current_user=current_user,
                           form=form, entry=entry)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!", "success")
    return redirect(url_for("login"))

def save_profile_image(profile_image):
    picture_file = os.path.splitext(profile_image.filename) # This returns a tuple of file name and the extension
    new_file_name = (f"{current_user.email_username}_{picture_file[0]}_"
                     f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                     f"{picture_file[1]}")
    safe_file_name = ""
    for i in range(0, len(new_file_name)):
        if new_file_name[i].isspace():
            safe_file_name += "_"
        else:
            safe_file_name += new_file_name[i]
    picture_path = os.path.join(app.root_path, "static/Images/profile_images", safe_file_name)
    # Resizing the image
    new_image = Image.open(profile_image)
    new_image_size = (240, 240)
    new_image.thumbnail(new_image_size)
    new_image.save(picture_path)
    return safe_file_name

def delete_old_image():
    old_image_path = f"static/Images/profile_images/{current_user.image_file}"
    if os.path.exists(old_image_path):
        if current_user.image_file != "Default - user.jpg" and current_user.image_file != "Default - user.png":
            os.remove(old_image_path)

@app.route("/user", methods=["GET", "POST"])
@login_required # It means we can access this route only if a user is logged in
def user():
    form = UpdateForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.picture_file.data:
                picture_file_name = save_profile_image(form.picture_file.data)
                delete_old_image()
                current_user.image_file = picture_file_name
            current_user.email_username = form.email_username.data
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