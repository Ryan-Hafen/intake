import phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from srs_intake.models import Facility, User, Referral

state_list = [('AL','Alabama'),('AK','Alaska'),('AZ','Arizona'),('AR','Arkansas'),('CA','California'),('CO','Colorado'),('CT','Connecticut'),('DE','Delaware'),('DC','District Of Columbia'),('FL','Florida'),('GA','Georgia'),('HI','Hawaii'),('ID','Idaho'),('IL','Illinois'),('IN','Indiana'),('IA','Iowa'),('KS','Kansas'),('KY','Kentucky'),('LA','Louisiana'),('ME','Maine'),('MD','Maryland'),('MA','Massachusetts'),('MI','Michigan'),('MN','Minnesota'),('MS','Mississippi'),('MO','Missouri'),('MT','Montana'),('NE','Nebraska'),('NV','Nevada'),('NH','New Hampshire'),('NJ','New Jersey'),('NM','New Mexico'),('NY','New York'),('NC','North Carolina'),('ND','North Dakota'),('OH','Ohio'),('OK','Oklahoma'),('OR','Oregon'),('PA','Pennsylvania'),('RI','Rhode Island'),('SC','South Carolina'),('SD','South Dakota'),('TN','Tennessee'),('TX','Texas'),('UT','Utah'),('VT','Vermont'),('VA','Virginia'),('WA','Washington'),('WV','West Virginia'),('WI','Wisconsin'),('WY','Wyoming')]
source_list = [('alf','ALF'),('hospital','Hospital'),('pcp','PCP'),('snf','SNF'),('specialist','Specialist')]
med_type_list = [('physician','Physician'),('np','NP'),('pa','PA')]

def validate_phone(form, field):
    try:
        p = phonenumbers.parse(field.data,"US")
        if not phonenumbers.is_valid_number(p):
            raise ValueError()
    except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
        raise ValidationError('Invalid phone number')   
     
     
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[Email()])
    phone = StringField('Phone', [validate_phone])
    fax = StringField('Fax', [validate_phone])
    submit = SubmitField('Send Request')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')    
        
class UserForm(FlaskForm):
    facilities = Facility.query.all()

    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[Email()])
    phone = StringField('Phone', [validate_phone])
    fax = StringField('Fax', [validate_phone])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('facility', 'Facility')])
    facility_id = SelectField('Facility', coerce=int, choices=[(i.id, i.name) for i in facilities])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Save')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        
class FacilityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    address1 = StringField('Address 1', validators=[Length(min=2, max=20)])
    address2 = StringField('Address 2')
    city = StringField('City')
    state = SelectField('State',choices=state_list)
    zip_code = StringField('Zip Code')
    source= SelectField('Source',choices=source_list)
    submit = SubmitField('Save')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[Email()])
    phone = StringField('Phone', [validate_phone])
    fax = StringField('Fax', [validate_phone])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')   
        
class ReferralForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    ssn = StringField('SSN', validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone')
    email = StringField('Email')
    dob = DateField('Date of Birth')
    poa = StringField('P.O.A')
    contact = StringField('Contact')
    poa_address1 = StringField('P.O.A Address')
    city = StringField('City')
    state = SelectField('State',choices=state_list,default='CA')
    zip_code = StringField('Zip Code')
    medicare = StringField('Medicare', validators=[DataRequired(), Length(min=2, max=20)])
    secondary = StringField('Secondary', validators=[DataRequired(), Length(min=2, max=20)])
    notes = TextAreaField('Diagnosis / Reason for referral / Additional notes')
    disc_slp = BooleanField('SLP Speech - Language Pathology')
    disc_ot = BooleanField('OT Occupational Therapy')
    disc_pt = BooleanField('PT Physical Therapy')
    treat_oral = BooleanField('Treatment of Swallowing Dysfunction/ Oral Function')
    treat_speech = BooleanField('Treatment of Speech, Voice, and Language Deficits')
    treat_cognitive = BooleanField('Cognitive Skills Development')
    treat_caregiver = BooleanField('Caregiver Education')
    treat_dementia = BooleanField('Dementia Management/Caregiver Training')
    treat_adl = BooleanField('ADL Training/Safety')
    treat_safety = BooleanField('Home Safety Assessment')
    treat_upper_extremity = BooleanField('Upper Extremity Prosthetic or Orthotic  Fitting and Training')
    treat_ther_exercise = BooleanField('Therapeutic Exercise')
    treat_balance = BooleanField('Balance Training')
    treat_ther_activity = BooleanField('Therapeutic Activity')
    treat_coordination = BooleanField('Coordination Propioception Training')
    treat_transfer = BooleanField('Transfer Training')
    treat_range = BooleanField('Range of Motion')
    treat_massage = BooleanField('Manual Therapy/Massage')
    treat_pain = BooleanField('Pain Management')
    treat_wheelchair = BooleanField('Wheelchair Provision/Training')
    treat_lower_extremity = BooleanField('Lower Extremity Prosthetic or Orthotic  Fitting and Training')
    treat_cane = BooleanField('Provision of Assistive Device i.e. cane,  walker')
    treat_postural = BooleanField('Postural Training')
    treat_gait = BooleanField('Gait/Endurance Training')
    treat_other = BooleanField('Other')
    treat_other_desc = StringField('Other Description',default='')
    med_type = RadioField(choices=med_type_list)
    med_firstname = StringField('First Name')
    med_lastname = StringField('Last Name')
    med_npi = StringField('NPI')
    med_phone = StringField('Phone')
    med_fax = StringField('Fax')
    med_email = StringField('Email')
    med_address1 = StringField('Address 1')
    med_address2 = StringField('Address 2')
    med_city = StringField('City')
    med_state = SelectField('State',choices=state_list,default='CA')
    med_zip_code = StringField('Zip Code')
    submit = SubmitField('Save')