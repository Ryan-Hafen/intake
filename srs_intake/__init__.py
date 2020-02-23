import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd0fadee28187514ce8d4d43f40cb5284327e8e3d921a331636408dab3b9769e6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 's.ryan.hafen@gmail.com'
app.config['MAIL_PASSWORD'] = 'mmnmglazdhpemygl'
# app.config['protocol'] = 'smtp';
# app.config['smtp_host'] = 'smtp.gmail.com';
# app.config['smtp_port'] = 465;
# app.config['smtp_crypto'] = 'ssl';
# app.config['newline'] = "\r\n";  
# app.config['mailtype'] = 'html';
# app.config['priority'] = 5;


db = SQLAlchemy(app)# from .models import User, Facility, Referral
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail(app)