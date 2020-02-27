from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField
from wtforms.ext.sqlalchemy.orm import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from srs_intake.models import Facility, User
from srs_intake.utils import validate_phone


roles_list = [('admin', 'Admin'), ('facility', 'Facility')]

class UserForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@email.com"})
    phone = StringField('Phone',render_kw={"placeholder": "555-555-5555","pattern": "[0-9]{3}-[0-9]{3}-[0-9]{4}"})
    fax = StringField('Fax',render_kw={"placeholder": "555-555-5555"})
    role = SelectField('Role', choices=roles_list)
    facility_id = SelectField('Facility', coerce=int)
    submit = SubmitField('Save')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class UpdateUserForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@email.com"})
    phone = StringField('Phone',render_kw={"placeholder": "555-555-5555","pattern": "[0-9]{3}-[0-9]{3}-[0-9]{4}"})
    fax = StringField('Fax',render_kw={"placeholder": "555-555-5555"})
    role = SelectField('Role', choices=roles_list)
    facility_id = SelectField('Facility', coerce=int)
    submit = SubmitField('Save')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@email.com"})
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@email.com"})
    submit = SubmitField('Request Password Reset')    

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    submit = SubmitField('Reset Password')       

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')