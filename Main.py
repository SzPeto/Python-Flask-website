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

# Master *****************************************************************************************************
load_dotenv()
app = Flask(__name__)
weather_app_object = WeatherApp()
functions = Functions()
is_first_log = True
# Get it like : secrets.token_hex(16)
app.config.update({"SECRET_KEY":os.environ.get("APP_SECRET_KEY")})
app.config.update({"SQLALCHEMY_DATABASE_URI":"sqlite:///database.db"})
db.init_app(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager.init_app(app)
login_manager.login_view = "login" # if someone tries to access a @login_required route
login_manager.login_message_category = "info"
# Mailing
app.config.update({
    "MAIL_SERVER": "smtp.googlemail.com",
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USERNAME": os.environ.get("EMAIL_USERNAME"),
    "MAIL_PASSWORD": os.environ.get("EMAIL_PASSWORD"),
})
print(f"{os.environ.get("EMAIL_USERNAME")}, {os.environ.get("EMAIL_PASSWORD")}")
mail = Mail(app)

# Main *******************************************************************************************************
if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        functions.write_log("******************************* Initial run *******************************************")
        is_first_log = False

    with app.app_context():
        db.create_all()

    from routes import *
    app.run(host = "0.0.0.0", debug=True)