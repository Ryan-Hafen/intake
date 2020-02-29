import phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, TextAreaField, RadioField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email


state_list = [('AL','Alabama'),('AK','Alaska'),('AZ','Arizona'),('AR','Arkansas'),('CA','California'),('CO','Colorado'),('CT','Connecticut'),('DE','Delaware'),('DC','District Of Columbia'),('FL','Florida'),('GA','Georgia'),('HI','Hawaii'),('ID','Idaho'),('IL','Illinois'),('IN','Indiana'),('IA','Iowa'),('KS','Kansas'),('KY','Kentucky'),('LA','Louisiana'),('ME','Maine'),('MD','Maryland'),('MA','Massachusetts'),('MI','Michigan'),('MN','Minnesota'),('MS','Mississippi'),('MO','Missouri'),('MT','Montana'),('NE','Nebraska'),('NV','Nevada'),('NH','New Hampshire'),('NJ','New Jersey'),('NM','New Mexico'),('NY','New York'),('NC','North Carolina'),('ND','North Dakota'),('OH','Ohio'),('OK','Oklahoma'),('OR','Oregon'),('PA','Pennsylvania'),('RI','Rhode Island'),('SC','South Carolina'),('SD','South Dakota'),('TN','Tennessee'),('TX','Texas'),('UT','Utah'),('VT','Vermont'),('VA','Virginia'),('WA','Washington'),('WV','West Virginia'),('WI','Wisconsin'),('WY','Wyoming')]
med_type_list = [('physician','Physician'),('np','NP'),('pa','PA')]


class ReferralForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    ssn = PasswordField('SSN', validators=[DataRequired(), Length(min=11, max=11)], render_kw={"placeholder": "111-22-3333","pattern": "[0-9]{3}-[0-9]{2}-[0-9]{4}"})
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10)], render_kw={"placeholder": "5555555555","pattern": "[0-9]{10}"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@email.com"})
    dob = DateField('Date of Birth')
    poa = StringField('P.O.A')
    contact = StringField('Contact')
    poa_address1 = StringField('P.O.A Address')
    city = StringField('City')
    state = SelectField('State',choices=state_list,default='CA')
    zip_code = StringField('Zip Code')
    medicare = StringField('Medicare', validators=[DataRequired(), Length(min=2, max=20)])
    secondary = StringField('Secondary Insurance')
    discharge_date = DateField('Discharge Date')
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
    med_type = RadioField(choices=med_type_list,validators=[DataRequired()])
    med_firstname = StringField('First Name',validators=[DataRequired()])
    med_lastname = StringField('Last Name',validators=[DataRequired()])
    med_npi = StringField('NPI',validators=[DataRequired()])
    med_phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10)], render_kw={"placeholder": "5555555555","pattern": "[0-9]{10}"})
    med_fax = StringField('Fax', validators=[Length(min=0, max=10)], render_kw={"placeholder": "3334445555"})
    med_email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@email.com"})
    med_address1 = StringField('Address 1',validators=[DataRequired()])
    med_address2 = StringField('Address 2')
    med_city = StringField('City',validators=[DataRequired()])
    med_state = SelectField('State',choices=state_list,default='CA',validators=[DataRequired()])
    med_zip_code = StringField('Zip Code',validators=[DataRequired()])
    submit = SubmitField('Save')