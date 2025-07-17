from flask_mail import Mail, Message

# app is a Flask app
app.config.update({
    "MAIL_SERVER": "smtp.googlemail.com",
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USERNAME": os.environ.get("EMAIL_USERNAME"),
    "MAIL_PASSWORD": os.environ.get("EMAIL_PASSWORD"),
})
mail = Mail(app)

msg = Message("Password reset requets", 
               sender="info.peterszepesi@gmail.com", 
               recipients=[user.email_username])
msg.body = f"""
To reset your password, please go to the following link : {url_for('password_reset_verified', token=token, _external=True)}
If you didn't make this request, simply ignore this email and no changes will be done.
"""
mail.send(msg)

# Important note
"""
Here in the password environment variable you have to set up the google app password, the regular password
won't work here, in order to get it, you have to have the 2 step verification in google account enabled, then access it
via link : myaccount.google.com/apppasswords
"""
