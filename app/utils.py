import os
import secrets
from flask import url_for, current_app, render_template
from flask_mail import Message
from app import mail


def send_email(subject, sender, recipients, html_body):
    try:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.html = html_body
        mail.send(msg)
    except Exception as e:
        return(str(e))

def send_new_account_email(user):
    token=user.get_new_user_token()
    send_email('An account has been created for you to user SacRehabSolutions.app.',
               'noreply@sacrehabsolutions.com',
               [user.email],
               render_template("mail/new_account.html", user=user, token=token))
    
def send_reset_email(user):
    token=user.get_reset_token()
    send_email('An account has been created for you to user SacRehabSolutions.app.',
               'noreply@sacrehabsolutions.com',
               [user.email],
               render_template("mail/reset_password.html", user=user, token=token))

def send_new_referral_email(referral, sender):
    send_email('New Patient Referral.',
               [sender],
               'noreply@sacrehabsolutions.com',
               render_template("mail/new_referral.html", referral=referral))

def send_completed_referral_email(referral, recipients):
    send_email('The referral for {referral.firstname} {referral.lastname} has been completed.',
               'noreply@sacrehabsolutions.com',
               [recipients],
               render_template("mail/reset_password.html", referral=referral))
