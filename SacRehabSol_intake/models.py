from datetime import datetime 
from SacRehabSol_intake import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    address1 = db.Column(db.String(120), unique=True, nullable=False)
    address2 =db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(20), unique=True, nullable=False)
    state = db.Column(db.String(2), unique=True, nullable=False)
    zip_code = db.Column(db.String(10), unique=True, nullable=False)
    source = db.Column(db.String(10), unique=True, nullable=False)
    users = db.relationship('User', backref='submitter', lazy=True)
    referals = db.relationship('Referral', backref='intake', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.city}', '{self.state}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=True, nullable=False)
    lastname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    fax = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.username}', {self.role}', {self.firstname}', '{self.lastname}')"    


class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    address1 = db.Column(db.String(120), nullable=True)
    address2 =db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(20), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    fax = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.DateTime, nullable=False)
    ssn = db.Column(db.String(20), unique=True, nullable=False)
    medicare = db.Column(db.String(20), unique=True, nullable=False)
    secondary = db.Column(db.String(20), unique=True, nullable=False)
    discharge_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(255), nullable=True)
    disc_slp = db.Column(db.boolean, nullable=False, default=0)
    disc_ot = db.Column(db.boolean, nullable=False, default=0)
    disc_pt = db.Column(db.boolean, nullable=False, default=0)
    treat_oral = db.Column(db.boolean, nullable=False, default=0)
    treat_speech = db.Column(db.boolean, nullable=False, default=0)
    treat_cognitive = db.Column(db.boolean, nullable=False, default=0)
    treat_caregiver = db.Column(db.boolean, nullable=False, default=0)
    treat_dementia = db.Column(db.boolean, nullable=False, default=0)
    treat_adl = db.Column(db.boolean, nullable=False, default=0)
    treat_safety = db.Column(db.boolean, nullable=False, default=0)
    treat_upper_extremity = db.Column(db.boolean, nullable=False, default=0)
    treat_ther_exercise = db.Column(db.boolean, nullable=False, default=0)
    treat_balance = db.Column(db.boolean, nullable=False, default=0)
    treat_ther_activity = db.Column(db.boolean, nullable=False, default=0)
    treat_coordination = db.Column(db.boolean, nullable=False, default=0)
    treat_transfer = db.Column(db.boolean, nullable=False, default=0)
    treat_range = db.Column(db.boolean, nullable=False, default=0)
    treat_massage = db.Column(db.boolean, nullable=False, default=0)
    treat_pain = db.Column(db.boolean, nullable=False, default=0)
    treat_wheelchair = db.Column(db.boolean, nullable=False, default=0)
    treat_lower_extremity = db.Column(db.boolean, nullable=False, default=0)
    treat_cane = db.Column(db.boolean, nullable=False, default=0)
    treat_postural = db.Column(db.boolean, nullable=False, default=0)
    treat_gait = db.Column(db.boolean, nullable=False, default=0)
    treat_other = db.Column(db.boolean, nullable=False, default=0)
    treat_other_desc = db.Column(db.String(120), nullable=True)
    med_firstname = db.Column(db.String(20), nullable=False)
    med_lastname = db.Column(db.String(20), nullable=False)
    med_address1 = db.Column(db.String(120), nullable=True)
    med_address2 =db.Column(db.String(120), nullable=True)
    med_city = db.Column(db.String(20), nullable=True)
    med_state = db.Column(db.String(2), nullable=True)
    med_zip_code = db.Column(db.String(10), nullable=True)
    med_email = db.Column(db.String(120), nullable=True)
    med_phone = db.Column(db.String(20), nullable=True)
    med_fax = db.Column(db.String(20), nullable=True)
    med_npi = db.Column(db.String(10), nullable=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"  