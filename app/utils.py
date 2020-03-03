import os
import secrets
from flask import url_for, current_app, render_template
from flask_mail import Message
from app import mail


def send_email(subject, sender, recipients, text_body, html_body):
    try:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        mail.send(msg)
    except Exception as e:
        return(str(e))

def send_new_account_email(user):
    token=user.get_new_user_token()
    send_email('An account has been created for you to user SacRehabSolutions.app.',
               'noreply@sacrehabsolutions.com',
               [user.email],
               render_template("mail/new_account.txt", user=user, token=token),
               render_template("mail/new_account.html", user=user, token=token))
    
def send_reset_email(user):
    token=user.get_reset_token()
    send_email('An account has been created for you to user SacRehabSolutions.app.',
               'noreply@sacrehabsolutions.com',
               [user.email],
               render_template("mail/reset_password.txt", user=user, token=token),
               render_template("mail/reset_password.html", user=user, token=token))

def send_new_referral_email(referral, sender):
    token=user.get_reset_token()
    send_email('New Patient Referral.',
               [sender],
               'noreply@sacrehabsolutions.com',
               render_template("mail/new_referral.txt", referral=referral),
               render_template("mail/new_referral.html", referral=referral))

def send_completed_referral_email(referral, recipients):
    token=user.get_reset_token()
    send_email('The referral for {referral.firstname} {referral.lastname} has been completed.',
               'noreply@sacrehabsolutions.com',
               [recipients],
               render_template("mail/reset_password.txt", referral=referral),
               render_template("mail/reset_password.html", referral=referral))
