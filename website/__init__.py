
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail

from website.config import Config
from website.db_models import db, login_manager
from website.weather_app.weather_app import WeatherApp
from website.main.functions import Functions

weather_app_object = WeatherApp()
functions = Functions()
bcrypt = Bcrypt()
csrf = CSRFProtect()
mail = Mail()

def create_app(config_class=Config):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "users_bp.login" # if someone tries to access a @login_required route
    login_manager.login_message_category = "info"
    mail.init_app(app)

    from website.weather_app.routes import weather_app_bp
    from website.users.routes import users_bp
    from website.blog.routes import blog_bp
    from website.main.routes import main_bp
    app.register_blueprint(weather_app_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(main_bp)

    return app