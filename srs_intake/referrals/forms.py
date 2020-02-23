import phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, TextAreaField, RadioField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email
from srs_intake.utils import validate_phone


state_list = [('AL','Alabama'),('AK','Alaska'),('AZ','Arizona'),('AR','Arkansas'),('CA','California'),('CO','Colorado'),('CT','Connecticut'),('DE','Delaware'),('DC','District Of Columbia'),('FL','Florida'),('GA','Georgia'),('HI','Hawaii'),('ID','Idaho'),('IL','Illinois'),('IN','Indiana'),('IA','Iowa'),('KS','Kansas'),('KY','Kentucky'),('LA','Louisiana'),('ME','Maine'),('MD','Maryland'),('MA','Massachusetts'),('MI','Michigan'),('MN','Minnesota'),('MS','Mississippi'),('MO','Missouri'),('MT','Montana'),('NE','Nebraska'),('NV','Nevada'),('NH','New Hampshire'),('NJ','New Jersey'),('NM','New Mexico'),('NY','New York'),('NC','North Carolina'),('ND','North Dakota'),('OH','Ohio'),('OK','Oklahoma'),('OR','Oregon'),('PA','Pennsylvania'),('RI','Rhode Island'),('SC','South Carolina'),('SD','South Dakota'),('TN','Tennessee'),('TX','Texas'),('UT','Utah'),('VT','Vermont'),('VA','Virginia'),('WA','Washington'),('WV','West Virginia'),('WI','Wisconsin'),('WY','Wyoming')]
med_type_list = [('physician','Physician'),('np','NP'),('pa','PA')]


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