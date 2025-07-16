import datetime
import os
import time
from typing import List
from flask import request, url_for
from flask_login import current_user
from flask_mail import Message
from PIL import Image
import requests

from website import mail, functions, login_attempts

def save_profile_image(profile_image):
    from run import app
    picture_file = os.path.splitext(profile_image.filename) # This returns a tuple of file name and the extension
    new_file_name = (f"{current_user.email_username}_{picture_file[0]}_"
                     f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                     f"{picture_file[1]}")
    safe_file_name = ""
    for i in range(0, len(new_file_name)):
        if new_file_name[i].isspace():
            safe_file_name += "_"
        else:
            safe_file_name += new_file_name[i]
    picture_path = os.path.join(app.root_path, "static", "Images", "profile_images", safe_file_name)
    # Resizing the image
    new_image = Image.open(profile_image)
    new_image_size = (240, 240)
    new_image.thumbnail(new_image_size)
    new_image.save(picture_path)
    return safe_file_name

def delete_old_image():
    from run import app
    old_image_path = os.path.join(app.root_path, "static", "Images", "profile_images", current_user.image_file)
    if os.path.exists(old_image_path):
        if current_user.image_file != "Default - user.jpg" and current_user.image_file != "Default - user.png":
            os.remove(old_image_path)

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        response.raise_for_status()
        data = response.json()
        return f"Country : {data.get('country')}"
    except Exception as e:
        functions.write_log(f"def get_ip_info : {e}")
        return ""

def get_client_info():
    # Check the real IP, if behind proxy, x_forwarded_for finds the real IP
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip() # Splits the ip addresses into a list where commas, than we acces the first
    else:
        ip = request.remote_addr
    # Agent
    agent = request.headers.get("User-Agent", "Unknown")
    browser_language = request.headers.get("Accept-Language")
    ip_info = get_ip_info(ip)
    return f"IP : {ip}, Agent : {agent}, Browser language : {browser_language}, {ip_info}"

def send_reset_mail(user):
    token = user.get_reset_token()
    msg = Message("Password reset requets", 
                  sender="info.peterszepesi@gmail.com", 
                  recipients=[user.email_username])
    # _external in body means, the entire link should be returned insted of only the relative
    msg.body = f"""
To reset your password, please go to the following link : {url_for('users_bp.password_reset_verified', token=token, _external=True)}
If you didn't make this request, simply ignore this email and no changes will be done.
"""
    mail.send(msg)

def check_login_attempts():
    # Setting the current time in seconds
    now = int((time.time_ns()) / 1000000000)

    # Getting the IP
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip() # Splits the ip addresses into a list where commas, than we acces the first
    else:
        ip = request.remote_addr
    
    # Registering the attempt
    if ip in login_attempts:
        login_attempts.get(ip).append(now)
    else:
        login_attempts.update({ip:[now]})
    
    # Deleting older than a minute attempts
    current_ip_attempts = login_attempts.get(ip)
    modified_ip_attempts = []
    for attempt_time in current_ip_attempts:
        if (now - attempt_time) < 60:
            modified_ip_attempts.append(attempt_time)
    login_attempts.update({ip:modified_ip_attempts})

    if len(login_attempts.get(ip)) <= 5:
        return True
    
    return False