from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import current_user
from app import db
from app.models import User, Referral, Source

main = Blueprint('main', __name__)



@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('referrals.list_referrals'))
    return redirect(url_for('users.login'))
