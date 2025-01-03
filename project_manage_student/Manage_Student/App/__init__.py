from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_mail import  Mail

app = Flask(__name__)
app.secret_key = "#@$^^$%$$jdhgfshfidsfjsifjs"
# extension of file
ALLOW_EXTENSIONS = {'xlsx'}
#connect database
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:%s@localhost/managestudent?charset=utf8mb4" %quote("Admin123@")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


# vnpay settings
app.config['VNP_TMN_CODE'] = 'A14L2WEK'
app.config['VNP_HASH_SECRET'] = 'GV06EKUKINLN1GSMO8LNHJSOY3G6AVKQ'
app.config['VNP_URL'] = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'
app.config['VNP_IP_ADDRESS'] = "127.0.0.1"
app.config['VNP_CURRENCY_CODE'] = 'VND'
app.config['VNP_VERSION'] = '2.1.0'
app.config['VNP_COMMAND'] = 'pay'

# mail server settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'cnatrocode@gmail.com'
app.config['MAIL_PASSWORD'] = 'rzzl lcju fnel qzuw'


# user login
app.config['USER_STAFF'] = 'staff'
app.config['USER_TEACHER'] = 'teacher'

db = SQLAlchemy(app)
login = LoginManager(app)
mail = Mail(app)

