import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from cryptography.fernet import Fernet
from flask_login import LoginManager
from flask_mail import Mail
from datetime import timedelta

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'd0fadee28187514ce8d4d43f40cb5284327e8e3d921a331636408dab3b9769e6'
app.config['ENCRYPT_KEY'] = b'KsDHbgWcUXBgP15mJ-ZAYG9LRd3dx90-aGYvZJ3wBHc='
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'admin@sacrehabsolutions.com'
app.config['MAIL_PASSWORD'] = 'hxpixdgravilxsjx'


db = SQLAlchemy(app)# from .models import User, Source, Referral
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
login_manager.refresh_view = 'users.login'
login_manager.needs_refresh_message = (u"Session timedout, please re-login")
login_manager.needs_refresh_message_category = "info"
mail = Mail(app)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=120)