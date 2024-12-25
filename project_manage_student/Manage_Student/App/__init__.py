from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "#@$^^$%$$jdhgfshfidsfjsifjs"
# extension of file
ALLOW_EXTENSIONS = {'xlsx'}
#connect database
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:%s@localhost/managestudent?charset=utf8mb4" %quote("011004")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config['QUANTITY_STUDENT'] = 20


# user login
app.config['USER_STAFF'] = 'staff'
app.config['USER_TEACHER'] = 'teacher'

db = SQLAlchemy(app)
login = LoginManager(app)

