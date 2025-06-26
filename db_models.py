import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="static/Images/Default-user.jpg")
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self) -> str:
        return f"User : {self.id}, {self.username_email}"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_posted = db.Column(db.String(12), nullable=False, default=datetime.datetime.now().strftime("%Y-%m-%d"))
    content = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Blog post : {self.id}, {self.title}, {self.date_posted}"