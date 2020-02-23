from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import current_user
from srs_intake import db
from srs_intake.models import User, Referral, Facility

main = Blueprint('main', __name__)



@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        if user.role == 'facility':
            referrals = Referral.query.filter_by(facility_id=user.facility_id)
            return render_template('referrals/referral_list.html', title="Referrals", referrals=referrals)
        if user.role == 'admin':
            referrals = Referral.query.all()
            return render_template('referrals/referral_list.html', title="Referrals", referrals=referrals)
    return redirect(url_for('users.login'))
