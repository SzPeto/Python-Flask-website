from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class PostForm(FlaskForm):
    post_title = StringField("Post title", validators=[DataRequired()])
    post_content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")