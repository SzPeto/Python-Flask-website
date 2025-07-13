from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, length
from flask_login import current_user

from db_models import User

# TODO - complete the reset and change password

class RegistrationForm(FlaskForm):
    email_username = StringField("Email - username", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    # The name after validate_ must match the field name in order for the function to be called email_username
    # It raises an error, so it won't validate on submit, this way a flash message will display the message
    # we specify here inside parentheses after ValidationError
    def validate_email_username(self, email_username):
        # email_username is a wtform object, so in order to get the name, call email_username.data
        existing_user = User.query.filter_by(email_username=email_username.data).first()
        if existing_user:
            raise ValidationError(f"{existing_user.email_username} is already taken, please choose another!")

class LoginForm(FlaskForm):
    email_username = StringField("Email - username", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    remember = BooleanField("Remember login")
    submit = SubmitField("Login")

class UpdateForm(FlaskForm):
    email_username = StringField("Email - username", validators=[DataRequired(), Email()])
    picture_file = FileField("Change profile picture", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    def validate_email_username(self, email_username):
        # email_username is a wtform object, so in order to get the name, call email_username.data
        if current_user.email_username != email_username.data:
            existing_user = User.query.filter_by(email_username=email_username.data).first()
            if existing_user:
                raise ValidationError(f"{existing_user.email_username} is already taken, please choose another!")

class PostForm(FlaskForm):
    post_title = StringField("Post title", validators=[DataRequired()])
    post_content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PasswordResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request password")

    def validate_email(self, email):
        email = User.query.filter_by(email_username=self.email.data).first()
        if email is None:
            raise ValidationError(f"Error, the email {email} isn't registered")

class PasswordResetUpdateForm(FlaskForm):
    new_password = PasswordField("New password", validators=[DataRequired()])
    new_password_confirm = PasswordField("Confirm new password", validators=[DataRequired(),
                                                                                   EqualTo("new_password")])
    submit = SubmitField("Submit")

class PasswordUpdateForm(FlaskForm):
    current_password = PasswordField("Current password", validators=[DataRequired(), Length(min=6)])
    new_password = PasswordField("New password", validators=[DataRequired()])
    new_password_confirm = PasswordField("Confirm new password", validators=[DataRequired(),
                                                                                   EqualTo("new_password")])
    submit = SubmitField("Submit")