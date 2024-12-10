from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "#@$^^$%$$jdhgfshfidsfjsifjs"
# extension of file
ALLOW_EXTENSIONS = {'xlsx'}
#connect database
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:%s@localhost/managestudent?charset=utf8mb4" %quote("Admin123@")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['QUANTITY_STUDENT'] = 20

db = SQLAlchemy(app)
login = LoginManager(app)

