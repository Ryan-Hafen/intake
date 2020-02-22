import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from srs_intake import app, db, bcrypt, mail
from srs_intake.forms import RegistrationForm, LoginForm, UserForm, FacilityForm, AccountForm, ReferralForm, RequestResetForm, ResetPasswordForm
from srs_intake.models import Facility, User, Referral
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    facilities = Facility.query.all()
    return render_template('home.html', facilities=facilities)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(firstname=form.firstname.data,lastname=form.lastname.data, email=form.email.data, phone=form.phone.data, fax=form.fax.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/user/new", methods=['GET', 'POST'])
# @login_required
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data,lastname=form.lastname.data, email=form.email.data, phone=form.phone.data, fax=form.fax.data, role=form.role.data, facility_id=form.facility_id.data, username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('The User was created successfully.', 'success')
        return redirect(url_for('login'))
    return render_template('create_user.html', title='Create User', form=form)


@app.route("/user/<int:user_id>")
# @login_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', title=f"{user.firstname} {user.lastname}", user=user)


@app.route("/user/<int:user_id>/update", methods=['GET', 'POST'])
# @login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    # if referral.facility_id != current_user.facility_id or current_user.role != 'admin':
    #     abort(403)
    form = UserForm()
    if form.validate_on_submit():
        user.firstname=form.firstname.data
        user.lastname=form.lastname.data
        user.email=form.email.data
        user.phone=form.phone.data
        user.fax=form.fax.data
        user.role=form.role.data
        user.username=form.username.data
        user.facility_id=form.facility_id.data
        db.session.commit()
        flash('The User was updated successfully.', 'success')
        return redirect(url_for('user',user_id=user_id))
    elif request.method == 'GET':
        form.firstname.data=user.firstname
        form.lastname.data=user.lastname
        form.email.data=user.email
        form.phone.data=user.phone
        form.fax.data=user.fax
        form.role.data=user.role
        form.username.data=user.username
        form.facility_id.data=user.facility_id
    return render_template('update_user.html', title='Update User', form=form)

@app.route("/user/<int:user_id>/delete", methods=['POST'])
# @login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # if referral.facility_id != current_user.facility_id or current_user.role != 'admin':
    #     abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('The User was deleted successfully.', 'success')
    return redirect(url_for('home'))


@app.route("/facility/new", methods=['GET', 'POST'])
# @login_required
def new_facility():
    form = FacilityForm()
    if form.validate_on_submit():
        facility = Facility(name=form.name.data,address1=form.address1.data, address2=form.address2.data, city=form.city.data, state=form.state.data, zip_code=form.zip_code.data, source=form.source.data)
        db.session.add(facility)
        db.session.commit()
        flash('The Facility was created successfully.', 'success')
        return redirect(url_for('login'))
    return render_template('crud_facility.html', title='Create Facility', form=form)


@app.route("/facility/<int:facility_id>")
# @login_required
def facility(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    return render_template('facility.html', title=f"{facility.name}", facility=facility)


@app.route("/facility/<int:facility_id>/update", methods=['GET', 'POST'])
# @login_required
def update_facility(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    # if referral.facility_id != current_user.facility_id or current_user.role != 'admin':
    #     abort(403)
    form = FacilityForm()
    if form.validate_on_submit():
        facility.name=form.name.data
        facility.address1=form.address1.data
        facility.address2=form.address2.data
        facility.city=form.city.data
        facility.state=form.state.data
        facility.zip_code=form.zip_code.data
        facility.source=form.source.data
        db.session.commit()
        flash('The Facility was updated successfully.', 'success')
        return redirect(url_for('facility',facility_id=facility_id))
    elif request.method == 'GET':
        form.name.data=facility.name
        form.address1.data=facility.address1
        form.address2.data=facility.address2
        form.city.data=facility.city
        form.state.data=facility.state
        form.zip_code.data=facility.zip_code
        form.source.data=facility.source
    return render_template('crud_facility.html', title='Update Facility', form=form)

@app.route("/facility/<int:facility_id>/delete", methods=['POST'])
# @login_required
def delete_facility(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    # if referral.facility_id != current_user.facility_id or current_user.role != 'admin':
    #     abort(403)
    db.session.delete(facility)
    db.session.commit()
    flash('The Facility was deleted successfully.', 'success')
    return redirect(url_for('home'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        current_user.firstname.data = form.firstname
        current_user.lastname.data = form.lastname
        current_user.email.data = form.email
        current_user.phone.data = form.phone
        current_user.fax.data = form.fax
        current_user.username.data = form.username
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.fax.data = current_user.fax
        form.username.data = current_user.username
    return render_template('account.html', title='Update Account', form=form)


@app.route("/referral/new", methods=['GET', 'POST'])
# @login_required
def new_referral():
    form = ReferralForm()
    if form.validate_on_submit():
        user = User.query.get(1)
        fac = user.user_loc
        referral = Referral(firstname=form.firstname.data, lastname=form.lastname.data, ssn=form.ssn.data
                           , phone=form.phone.data, email=form.email.data, dob=form.dob.data
                           , poa=form.poa.data, contact=form.contact.data
                           , poa_address1=form.poa_address1.data
                           , city=form.city.data, state=form.state.data, zip_code=form.zip_code.data
                           , medicare=form.medicare.data, secondary=form.secondary.data
                           , notes=form.notes.data
                           , disc_slp=form.disc_slp.data, disc_ot=form.disc_ot.data, disc_pt=form.disc_pt.data
                           , treat_oral=form.treat_oral.data, treat_speech=form.treat_speech.data, treat_cognitive=form.treat_cognitive.data
                           , treat_caregiver=form.treat_caregiver.data, treat_dementia=form.treat_dementia.data, treat_adl=form.treat_adl.data
                           , treat_safety=form.treat_safety.data, treat_upper_extremity=form.treat_upper_extremity.data, treat_ther_exercise=form.treat_ther_exercise.data
                           , treat_balance=form.treat_balance.data, treat_ther_activity=form.treat_ther_activity.data, treat_coordination=form.treat_coordination.data
                           , treat_transfer=form.treat_transfer.data, treat_range=form.treat_range.data, treat_massage=form.treat_massage.data
                           , treat_pain=form.treat_pain.data, treat_wheelchair=form.treat_wheelchair.data, treat_lower_extremity=form.treat_lower_extremity.data
                           , treat_cane=form.treat_cane.data, treat_postural=form.treat_postural.data, treat_gait=form.treat_gait.data
                           , treat_other=form.treat_other.data, treat_other_desc=form.treat_other_desc.data
                           , med_type=form.med_type.data
                           , med_firstname=form.med_firstname.data, med_lastname=form.med_lastname.data, med_npi=form.med_npi.data
                           , med_phone=form.med_phone.data, med_fax=form.med_fax.data, med_email=form.med_email.data
                           , med_address1=form.med_address1.data
                           , med_address2=form.med_address2.data
                           , med_city=form.med_city.data, med_state=form.med_state.data, med_zip_code=form.med_zip_code.data
                           , user_id=user.id
                           , facility_id=fac.id)
        db.session.add(referral)
        db.session.commit()
        flash('The Referral was submitted successfully.', 'success')
        return redirect(url_for('home'))
    return render_template('crud_referral.html', title='Create Referral', form=form)


@app.route("/referral/<int:referral_id>")
# @login_required
def referral(referral_id):
    referral = Referral.query.get_or_404(referral_id)
    return render_template('referral.html', title=f"{referral.firstname} {referral.lastname}", referral=referral)


@app.route("/referral/<int:referral_id>/update", methods=['GET', 'POST'])
# @login_required
def update_referral(referral_id):
    referral = Referral.query.get_or_404(referral_id)
    # if referral.facility_id != current_user.facility_id or current_user.role != 'admin':
    #     abort(403)
    form = ReferralForm()
    if form.validate_on_submit():
        referral.firstname=form.firstname.data
        referral.lastname=form.lastname.data
        referral.ssn=form.ssn.data
        referral.phone=form.phone.data
        referral.email=form.email.data
        referral.dob=form.dob.data
        referral.poa=form.poa.data
        referral.contact=form.contact.data
        referral.poa_address1=form.poa_address1.data
        referral.city=form.city.data
        referral.state=form.state.data
        referral.zip_code=form.zip_code.data
        referral.medicare=form.medicare.data
        referral.secondary=form.secondary.data
        referral.notes=form.notes.data
        referral.disc_slp=form.disc_slp.data
        referral.disc_ot=form.disc_ot.data
        referral.disc_pt=form.disc_pt.data
        referral.treat_oral=form.treat_oral.data
        referral.treat_speech=form.treat_speech.data
        referral.reat_cognitive=form.treat_cognitive.data
        referral.treat_caregiver=form.treat_caregiver.data
        referral.treat_dementia=form.treat_dementia.data
        referral.treat_adl=form.treat_adl.data
        referral.treat_safety=form.treat_safety.data
        referral.treat_upper_extremity=form.treat_upper_extremity.data
        referral.treat_ther_exercise=form.treat_ther_exercise.data
        referral.treat_balance=form.treat_balance.data
        referral.treat_ther_activity=form.treat_ther_activity.data
        referral.treat_coordination=form.treat_coordination.data
        referral.treat_transfer=form.treat_transfer.data
        referral.treat_range=form.treat_range.data
        referral.treat_massage=form.treat_massage.data
        referral.treat_pain=form.treat_pain.data
        referral.treat_wheelchair=form.treat_wheelchair.data
        referral.treat_lower_extremity=form.treat_lower_extremity.data
        referral.treat_cane=form.treat_cane.data
        referral.treat_postural=form.treat_postural.data
        referral.treat_gait=form.treat_gait.data
        referral.treat_other=form.treat_other.data
        referral.treat_other_desc=form.treat_other_desc.data
        referral.med_type=form.med_type.data
        referral.med_firstname=form.med_firstname.data
        referral.med_lastname=form.med_lastname.data
        referral.med_npi=form.med_npi.data
        referral.med_phone=form.med_phone.data
        referral.med_fax=form.med_fax.data
        referral.med_email=form.med_email.data
        referral.med_address1=form.med_address1.data
        referral.med_address2=form.med_address2.data
        referral.med_city=form.med_city.data
        referral.med_state=form.med_state.data
        referral.med_zip_code=form.med_zip_code.data
        db.session.commit()
        flash('The Referral was updated successfully.', 'success')
        return redirect(url_for('referral',referral_id=referral_id))
    elif request.method == 'GET':
        form.firstname.data=referral.firstname
        form.lastname.data=referral.lastname
        form.ssn.data=referral.ssn
        form.phone.data=referral.phone
        form.email.data=referral.email
        form.dob.data=referral.dob
        form.poa.data=referral.poa
        form.contact.data=referral.contact
        form.poa_address1.data=referral.poa_address1
        form.city.data=referral.city
        form.state.data=referral.state
        form.zip_code.data=referral.zip_code
        form.medicare.data=referral.medicare
        form.secondary.data=referral.secondary
        form.notes.data=referral.notes
        form.disc_slp.data=referral.disc_slp
        form.disc_ot.data=referral.disc_ot
        form.disc_pt.data=referral.disc_pt
        form.treat_oral.data=referral.treat_oral
        form.treat_speech.data=referral.treat_speech
        form.treat_cognitive.data=referral.treat_cognitive
        form.treat_caregiver.data=referral.treat_caregiver
        form.treat_dementia.data=referral.treat_dementia
        form.treat_adl.data=referral.treat_adl
        form.treat_safety.data=referral.treat_safety
        form.treat_upper_extremity.data=referral.treat_upper_extremity
        form.treat_ther_exercise.data=referral.treat_ther_exercise
        form.treat_balance.data=referral.treat_balance
        form.treat_ther_activity.data=referral.treat_ther_activity
        form.treat_coordination.data=referral.treat_coordination
        form.treat_transfer.data=referral.treat_transfer
        form.treat_range.data=referral.treat_range
        form.treat_massage.data=referral.treat_massage
        form.treat_pain.data=referral.treat_pain
        form.treat_wheelchair.data=referral.treat_wheelchair
        form.treat_lower_extremity.data=referral.treat_lower_extremity
        form.treat_cane.data=referral.treat_cane
        form.treat_postural.data=referral.treat_postural
        form.treat_gait.data=referral.treat_gait
        form.treat_other.data=referral.treat_other
        form.treat_other_desc.data=referral.treat_other_desc
        form.med_type.data=referral.med_type
        form.med_firstname.data=referral.med_firstname
        form.med_lastname.data=referral.med_lastname
        form.med_npi.data=referral.med_npi
        form.med_phone.data=referral.med_phone
        form.med_fax.data=referral.med_fax
        form.med_email.data=referral.med_email
        form.med_address1.data=referral.med_address1
        form.med_address2.data=referral.med_address2
        form.med_city.data=referral.med_city
        form.med_state.data=referral.med_state
        form.med_zip_code.data=referral.med_zip_code
    return render_template('crud_referral.html', title='Update Referral', form=form)

@app.route("/referral/<int:referral_id>/delete", methods=['POST'])
# @login_required
def delete_referral(referral_id):
    referral = Referral.query.get_or_404(referral_id)
    # if referral.facility_id != current_user.facility_id or current_user.role != 'admin':
    #     abort(403)
    db.session.delete(referral)
    db.session.commit()
    flash('The Referral was deleted successfully.', 'success')
    return redirect(url_for('home'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                   sender='noreply@sacrehabsolutions.com', 
                   recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token',token=token,_external=True)}

If you did not request a password reset please ignore this email.
'''
    mail.send(msg)
                

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)  