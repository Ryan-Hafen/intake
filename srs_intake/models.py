from datetime import datetime
from flask import url_for, flash, redirect
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from srs_intake import app, db, login_manager
from flask_login import UserMixin

# Validating user login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Redirect unauthorized users to Login page.
@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.','info')
    return redirect(url_for('users.login'))  


class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    address1 = db.Column(db.String(120), nullable=True)
    address2 = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(20), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    source = db.Column(db.String(10), nullable=True)
    users = db.relationship('User', backref='user_loc', lazy=True)
    referals = db.relationship('Referral', backref='referral_loc', lazy=True)

    def __repr__(self):
        return f"Facility('{self.name}', '{self.city}', '{self.state}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=True)
    lastname = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    fax = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(60), nullable=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=True)
    facility = db.relationship('Facility', backref='submitter', lazy=True)


    # get reset token
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

        # get reset token
    def get_new_user_token(self, expires_sec=86400):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # Verify email reset token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.email}', {self.role}', {self.firstname}', '{self.lastname}')"    


class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referral_status = db.Column(db.String(20), nullable=True, default='new')
    firstname = db.Column(db.String(20), nullable=True)
    lastname = db.Column(db.String(20), nullable=True)
    ssn = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    dob = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    poa = db.Column(db.String(120), nullable=True)
    contact = db.Column(db.String(120), nullable=True)
    poa_address1 = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(20), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    medicare = db.Column(db.String(20), nullable=True)
    secondary = db.Column(db.String(20), nullable=True)
    discharge_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    notes = db.Column(db.String(255), nullable=True)
    disc_slp = db.Column(db.Boolean, nullable=True, default=False)
    disc_ot = db.Column(db.Boolean, nullable=True, default=False)
    disc_pt = db.Column(db.Boolean, nullable=True, default=False)
    treat_oral = db.Column(db.Boolean, nullable=True, default=False)
    treat_speech = db.Column(db.Boolean, nullable=True, default=False)
    treat_cognitive = db.Column(db.Boolean, nullable=True, default=False)
    treat_caregiver = db.Column(db.Boolean, nullable=True, default=False)
    treat_dementia = db.Column(db.Boolean, nullable=True, default=False)
    treat_adl = db.Column(db.Boolean, nullable=True, default=False)
    treat_safety = db.Column(db.Boolean, nullable=True, default=False)
    treat_upper_extremity = db.Column(db.Boolean, nullable=True, default=False)
    treat_ther_exercise = db.Column(db.Boolean, nullable=True, default=False)
    treat_balance = db.Column(db.Boolean, nullable=True, default=False)
    treat_ther_activity = db.Column(db.Boolean, nullable=True, default=False)
    treat_coordination = db.Column(db.Boolean, nullable=True, default=False)
    treat_transfer = db.Column(db.Boolean, nullable=True, default=False)
    treat_range = db.Column(db.Boolean, nullable=True, default=False)
    treat_massage = db.Column(db.Boolean, nullable=True, default=False)
    treat_pain = db.Column(db.Boolean, nullable=True, default=False)
    treat_wheelchair = db.Column(db.Boolean, nullable=True, default=False)
    treat_lower_extremity = db.Column(db.Boolean, nullable=True, default=False)
    treat_cane = db.Column(db.Boolean, nullable=True, default=False)
    treat_postural = db.Column(db.Boolean, nullable=True, default=False)
    treat_gait = db.Column(db.Boolean, nullable=True, default=False)
    treat_other = db.Column(db.Boolean, nullable=True, default=False)
    treat_other_desc = db.Column(db.String(120), nullable=True)
    med_type = db.Column(db.String(20), nullable=True)
    med_firstname = db.Column(db.String(20), nullable=True)
    med_lastname = db.Column(db.String(20), nullable=True)
    med_npi = db.Column(db.String(10), nullable=True)
    med_address1 = db.Column(db.String(120), nullable=True)
    med_address2 =db.Column(db.String(120), nullable=True)
    med_city = db.Column(db.String(20), nullable=True)
    med_state = db.Column(db.String(2), nullable=True)
    med_zip_code = db.Column(db.String(10), nullable=True)
    med_email = db.Column(db.String(120), nullable=True)
    med_phone = db.Column(db.String(20), nullable=True)
    med_fax = db.Column(db.String(20), nullable=True)
    referral_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=True)
    users = db.relationship('User', backref='user_ref', lazy=True)
    facility = db.relationship('Facility', backref='loc_ref', lazy=True)

    def __repr__(self):
        return f"Referral('{self.firstname}', '{self.lastname}', '{self.discharge_date}')" 