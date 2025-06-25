import datetime

from Main import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username_email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="static/Images/default-user.jpg")

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_posted = db.Column(db.String(12), nullable=False, default=datetime.datetime.now().strftime("%Y-%m-%d"))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column()