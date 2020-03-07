from datetime import datetime
from flask import url_for, flash, redirect
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from cryptography.fernet import Fernet, base64
from app import app, db, login_manager, bcrypt
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

# Source (one to many) User
# Source (one to many) Referral
# User (one to many) Referral

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    address1 = db.Column(db.String(120), nullable=True)
    address2 = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    source = db.Column(db.String(10), nullable=True)
    users = db.relationship('User', backref='source_user', lazy=True)
    referrals = db.relationship('Referral', backref='source_ref', lazy=True)

    def __repr__(self):
        return f"Source('{self.name}', '{self.city}', '{self.state}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    fax = db.Column(db.String(50), nullable=True)
    job_type = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(60), nullable=True, default=bcrypt.generate_password_hash(app.config['SECRET_KEY']).decode('utf-8'))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))


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
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    ssn = db.Column(db.BINARY(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    dob = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    poa = db.Column(db.String(120), nullable=True)
    poa_phone = db.Column(db.String(120), nullable=True)
    poa_address1 = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    medicare = db.Column(db.BINARY(255), nullable=True)
    secondary = db.Column(db.BINARY(255), nullable=True)
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
    med_type = db.Column(db.String(50), nullable=True)
    med_firstname = db.Column(db.String(50), nullable=True)
    med_lastname = db.Column(db.String(50), nullable=True)
    med_npi = db.Column(db.String(10), nullable=True)
    med_address1 = db.Column(db.String(120), nullable=True)
    med_address2 =db.Column(db.String(120), nullable=True)
    med_city = db.Column(db.String(50), nullable=True)
    med_state = db.Column(db.String(2), nullable=True)
    med_zip_code = db.Column(db.String(10), nullable=True)
    med_email = db.Column(db.String(120), nullable=True)
    med_phone = db.Column(db.String(50), nullable=True)
    med_fax = db.Column(db.String(50), nullable=True)
    referral_status = db.Column(db.String(50), nullable=True, autoincrement=True, default='new')
    referral_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
    users = db.relationship('User', backref='user_ref', lazy=True)
    source = db.relationship('Source', backref='loc_ref', lazy=True)

    # Encrypt
    def encrypt_data(field):
        e = field.encode()
        f = Fernet(app.config['ENCRYPT_KEY'])
        encrypted = f.encrypt(e)
        return encrypted

    # Decrypt
    def decrypt_data(field):
        d = field
        f = Fernet(app.config['ENCRYPT_KEY'])
        decrypted = f.decrypt(d).decode('utf-8')
        return decrypted
         

    def __repr__(self):
        return f"Referral('{self.firstname}', '{self.lastname}', '{self.discharge_date}')" 



