from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


state_list = [('AL','Alabama'),('AK','Alaska'),('AZ','Arizona'),('AR','Arkansas'),('CA','California'),('CO','Colorado'),('CT','Connecticut'),('DE','Delaware'),('DC','District Of Columbia'),('FL','Florida'),('GA','Georgia'),('HI','Hawaii'),('ID','Idaho'),('IL','Illinois'),('IN','Indiana'),('IA','Iowa'),('KS','Kansas'),('KY','Kentucky'),('LA','Louisiana'),('ME','Maine'),('MD','Maryland'),('MA','Massachusetts'),('MI','Michigan'),('MN','Minnesota'),('MS','Mississippi'),('MO','Missouri'),('MT','Montana'),('NE','Nebraska'),('NV','Nevada'),('NH','New Hampshire'),('NJ','New Jersey'),('NM','New Mexico'),('NY','New York'),('NC','North Carolina'),('ND','North Dakota'),('OH','Ohio'),('OK','Oklahoma'),('OR','Oregon'),('PA','Pennsylvania'),('RI','Rhode Island'),('SC','South Carolina'),('SD','South Dakota'),('TN','Tennessee'),('TX','Texas'),('UT','Utah'),('VT','Vermont'),('VA','Virginia'),('WA','Washington'),('WV','West Virginia'),('WI','Wisconsin'),('WY','Wyoming')]
source_list = [('alf','ALF'),('hospital','Hospital'),('pcp','PCP'),('snf','SNF'),('specialist','Specialist'),('sacrehab','Sac Rehab')]

class SourceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    address1 = StringField('Address 1', validators=[Length(min=2, max=20)])
    address2 = StringField('Address 2')
    city = StringField('City')
    state = SelectField('State',choices=state_list)
    zip_code = StringField('Zip Code')
    source= SelectField('Source',choices=source_list)
    submit = SubmitField('Save')