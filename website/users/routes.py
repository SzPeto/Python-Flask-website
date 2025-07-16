from flask import Blueprint, flash, request, redirect, url_for, render_template
from flask_login import login_user, current_user, login_required, logout_user

from website import functions, bcrypt
from website.users.validators import *
from website.users.utils import *
from website.db_models import User, Post, db

users_bp = Blueprint("users_bp", __name__)

# ==============================================================================================================================
#                                                     Register, login, logout
# ==============================================================================================================================

@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.index"))
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
            return redirect(url_for("users_bp.login"))
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
    
    return render_template("register.html", title="Register", form=form,
                           current_user=current_user)

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.index"))
    form = LoginForm()
    if request.method == "POST":
        # Checking the login attempts and setting a default per minute
        if not check_login_attempts():
            flash("Too many login attempts from your IP address, try again later!", "warning")
            functions.write_log(f"Invalid login - too many attempts : {form.email_username.data}, {get_client_info()}")
            return redirect(url_for("users_bp.login"))

        if form.validate_on_submit():
            # Getting the user based on entered email_username
            user = User.query.filter_by(email_username=form.email_username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    flash(f"Login successful! {form.email_username.data}", "success")
                    return redirect(url_for("main_bp.index"))
                else:
                    flash("Invalid password!", "warning")
                    functions.write_log(f"Invalid login - wrong password : {form.email_username.data}, {get_client_info()}")
            else:
                flash(f"{form.email_username.data} : account doesn't exist!", "warning")
                functions.write_log(f"Invalid login - wrong username : {form.email_username.data}, {get_client_info()}")

        else:
            if form.email_username.errors:
                for error in form.email_username.errors:
                    flash(f"Email - username : {error}", "warning")
            if form.password.errors:
                for error in form.password.errors:
                    flash(f"Password : {error}", "warning")

    return render_template("login.html", title="Login", form=form,
                           current_user=current_user)

@users_bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!", "success")
    return redirect(url_for("users_bp.login"))

@users_bp.route("/user", methods=["GET", "POST"])
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


# ==============================================================================================================================
#                                                     Password management
# ==============================================================================================================================



@users_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = PasswordUpdateForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            new_hashed_pw = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
            current_user.password = new_hashed_pw
            db.session.commit()
            flash("Password successfully updated", "success")
            return redirect(url_for("main_bp.index"))
        else:
            flash("You've entered a wrong current password", "warning")
    else:
        if form.current_password.errors:
            for error in form.current_password.errors:
                flash(f"Current password : {error}", "warning")
        if form.new_password.errors:
            for error in form.new_password.errors:
                flash(f"New password : {error}", "warning")
        if form.new_password_confirm.errors:
            for error in form.new_password_confirm.errors:
                flash(f"New password confirm : {error}", "warning")
            
    return render_template("change-password.html", title="Password change", current_user=current_user, form=form)

@users_bp.route("/password-reset", methods=["GET", "POST"])
def password_reset_initial():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.index"))
    form = PasswordResetForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            user = User.query.filter_by(email_username=email).first()
            if user:
                send_reset_mail(user)
                flash(f"The instructions to reset you password has been sent to : {email}", "success")
            else:
                flash("The mail you've entered doesn't exist in database", "warning")
        else:
            if form.email.errors:
                for error in form.email.errors:
                    flash(error, "warning")

    return render_template("password-reset-initial.html", title="Password reset", current_user=current_user,
                           form=form)

# In Flask you dont't have to explicitly define the string, by default a parameter is string
@users_bp.route("/password-reset/<token>", methods=["GET", "POST"])
def password_reset_verified(token):
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.index"))
    form = PasswordResetUpdateForm()
    user = User.verify_reset_token(token)
    if request.method == "POST":
        if form.validate_on_submit():
            encrypted_pw = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
            if user:
                user.password = encrypted_pw
                db.session.commit()
                flash("Password updated successfully!", "success")
                return redirect(url_for("users_bp.login"))
            else:
                flash("Sorry, it seems your token expired, please try again!", "warning")
                return redirect(url_for("users_bp.password_reset_initial"))
        else:
            if form.new_password.errors:
                for error in form.new_password.errors:
                    flash(error, "warning")
            if form.new_password_confirm.errors:
                for error in form.new_password_confirm.errors:
                    flash(error, "warning")

    if user:
        flash("Verification successful, now you can change your password", "success")
        return render_template("password-reset-verified.html", title="Password reset", user=user,
                           form=form)
    else:
        flash("Verification failed, the token is either invalid or it expired, please try again!",
              "warning")
        return redirect(url_for("users_bp.password_reset_initial"))
