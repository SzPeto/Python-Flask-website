from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, length
from db_models import User


class RegistrationForm(FlaskForm):
    email_username = StringField("Email - username", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    # The name after validate_ must match the field name in order for the function to be called email_username
    # It raises an error, so it won't validate on submit, this way a flash message will display the message
    # we specify here inside parentheses after ValidationError
    def validate_email_username(self, email_username):
        existing_user = User.query.filter_by(email_username=email_username.data).first()
        if existing_user:
            raise ValidationError(f"{existing_user.email_username} is already taken, please choose another!")

class LoginForm(FlaskForm):
    email_username = StringField("Email - username", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    remember = BooleanField("Remember login")
    submit = SubmitField("Login")