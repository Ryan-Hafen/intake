import os
import secrets
import phonenumbers
from flask import url_for, current_app
from flask_mail import Message
from srs_intake import mail



def send_new_account_email(user):
    token = user.get_reset_token()
    msg = Message('An account has been created for you to user SacRehabSolutions.app.', 
                   sender='noreply@sacrehabsolutions.com', 
                   recipients=[user.email])
    msg.body = f'''Please use your email ({user.email}) to reset your password by clicking on the link below.
{url_for('users.reset_token',token=token,_external=True)}

'''
    mail.send(msg)

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


def send_new_referral_email(referral, s_email):
    msg = Message('New Patient Referral', 
                   sender=s_email, 
                   recipients=['intake@sacrehabsolutions.com'])
    msg.body = f'''To view the referal, please visit the following link:
{url_for('referrals.referral',referral_id=referral.id,_external=True)}
'''
    mail.send(msg)


def send_completed_referral_email(referral, r_email):
    msg = Message(f'The referral for {referral.firstname} {referral.lastname} has been completed', 
                   sender='noreply@sacrehabsolutions.com', 
                   recipients=[r_email])
    msg.body = f'''To view the referal, please visit the following link:
{url_for('referrals.referral',referral_id=referral.id,_external=True)}
'''
    mail.send(msg)  


def validate_phone(form, field):
    try:
        p = phonenumbers.parse(field.data,"US")
        if not phonenumbers.is_valid_number(p):
            raise ValueError()
    except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
        raise ValidationError('Invalid phone number')     