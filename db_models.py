import datetime
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

# Setting up the login_manager
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# We have to inherit from class UserMixin, to get the user attributes :
# is_authenticated, is_active, is_anonymous and the get_id method
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="Default - user.jpg")
    posts = db.relationship("Post", backref="user", lazy=True)

    def __repr__(self) -> str:
        return f"User : {self.id}, {self.email_username}, {self.image_file}"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_posted = db.Column(db.String(22), nullable=False,
                            default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    content = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    # Here user.id is with lower, since SQLAlchemy converts automatically the class name to lower table name
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Blog post : {self.id}, {self.title}, {self.date_posted}"