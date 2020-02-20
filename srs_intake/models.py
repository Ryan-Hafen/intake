from datetime import datetime
from srs_intake import db

class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    address1 = db.Column(db.String(120), nullable=True)
    address2 =db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(20), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    source = db.Column(db.String(10), nullable=True)
    users = db.relationship('User', backref='user_loc', lazy=True)
    referals = db.relationship('Referral', backref='referral_loc', lazy=True)

    def __repr__(self):
        return f"Facility('{self.name}', '{self.city}', '{self.state}')"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=True)
    lastname = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    fax = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=True)
    facility = db.relationship('Facility', backref='submitter', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', {self.role}', {self.firstname}', '{self.lastname}')"    


class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=True)
    lastname = db.Column(db.String(20), nullable=True)
    address1 = db.Column(db.String(120), nullable=True)
    address2 =db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(20), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    fax = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    ssn = db.Column(db.String(20), unique=True, nullable=True)
    medicare = db.Column(db.String(20), unique=True, nullable=True)
    secondary = db.Column(db.String(20), unique=True, nullable=True)
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
    med_firstname = db.Column(db.String(20), nullable=True)
    med_lastname = db.Column(db.String(20), nullable=True)
    med_address1 = db.Column(db.String(120), nullable=True)
    med_address2 =db.Column(db.String(120), nullable=True)
    med_city = db.Column(db.String(20), nullable=True)
    med_state = db.Column(db.String(2), nullable=True)
    med_zip_code = db.Column(db.String(10), nullable=True)
    med_email = db.Column(db.String(120), nullable=True)
    med_phone = db.Column(db.String(20), nullable=True)
    med_fax = db.Column(db.String(20), nullable=True)
    med_npi = db.Column(db.String(10), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=True)
    users = db.relationship('User', backref='user_ref', lazy=True)
    facility = db.relationship('Facility', backref='loc_ref', lazy=True)

    def __repr__(self):
        return f"Referral('{self.firstname}', '{self.lastname}', '{self.discharge_date}')" 