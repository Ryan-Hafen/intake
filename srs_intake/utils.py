import os
import secrets
from flask import url_for, current_app
from flask_mail import Message
from srs_intake import mail



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                   sender='noreply@sacrehabsolutions.com', 
                   recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token',token=token,_external=True)}

If you did not request a password reset please ignore this email.
'''
    mail.send(msg)


def validate_phone(form, field):
    try:
        p = phonenumbers.parse(field.data,"US")
        if not phonenumbers.is_valid_number(p):
            raise ValueError()
    except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
        raise ValidationError('Invalid phone number')     