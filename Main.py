import os
from flask import Flask
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_mail import Mail

from functions import Functions
from weather_app import WeatherApp
import secrets

from db_models import db, login_manager

# TODO - set up the mail address and complete for it the environment variables

# Master *****************************************************************************************************
load_dotenv()
app = Flask(__name__)
weather_app_object = WeatherApp()
functions = Functions()
is_first_log = True
# Get it like : secrets.token_hex(16)
app.config.update({"SECRET_KEY":"a458918b381a3ee2a83cebfca2320ac0"})
app.config.update({"SQLALCHEMY_DATABASE_URI":"sqlite:///database.db"})
db.init_app(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager.init_app(app)
login_manager.login_view = "login" # if someone tries to access a @login_required route
login_manager.login_message_category = "info"
# Mailing
app.config.update({"MAIL_SERVER":"smtp.googlemail.com"})
app.config.update({"MAIL_PORT":587})
app.config.update({"MAIL_USE_TLS":True})
app.config.update({"MAIL_USERNAME":os.getenv("EMAIL_USERNAME")})
app.config.update({"MAIL_PASSWORD":os.getenv("EMAIL_PASSWORD")})

# Main *******************************************************************************************************
if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        functions.write_log("******************************* Initial run *******************************************")
        is_first_log = False

    with app.app_context():
        db.create_all()

    from routes import *
    app.run(host = "0.0.0.0", debug=True)