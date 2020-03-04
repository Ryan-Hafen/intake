from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import current_user
from app import db
from app.models import User, Referral, Source

main = Blueprint('main', __name__)



@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        if user.role == 'source':
            referrals = Referral.query.filter_by(source_id=user.source_id)
            return render_template('referrals/referral_list.html', title="Referrals")
        if user.role == 'admin':
            referrals = Referral.query.all()
            return render_template('referrals/referral_list.html', title="Referrals")
    return redirect(url_for('users.login'))
