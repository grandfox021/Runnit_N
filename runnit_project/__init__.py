from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy  # type: ignore
import secrets
from datetime import timedelta

app = Flask(__name__,template_folder="templates")

app.secret_key =secrets.token_hex(16)


DEFAULT_IMAGE_PATH_FOR_USER = "static/images/uploads/default_pic_for_user.png"
DEFAULT_IMAGE_PATH_FOR_POST = "static/images/uploads/default_pic_for_post.png" 
DEFAULT_IMAGE_PATH_FOR_COURSE = "static/images/uploads/default_pic_for_course.png" 

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)

DEFAULT_PATH_FOR_RESUME = "runnit_project/static/resume_uploads" 

UPLOAD_FOLDER = 'runnit_project/static/images/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# Twilio credentials
TWILIO_ACCOUNT_SID = 'ACa916e0171cb19f5f9ee1988dafa48ee3'
TWILIO_AUTH_TOKEN = '0e1c876c17e02f100cd6f25943afdf00'
TWILIO_PHONE_NUMBER = '(512)710-1831'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'hbsmtp635@gmail.com'
app.config['MAIL_PASSWORD'] = 'ylgt aavy aawr gwwg'
app.config['MAIL_DEFAULT_SENDER'] = 'hbsmtp635@gmail.com'




from . import routes