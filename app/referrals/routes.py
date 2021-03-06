from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_user, current_user, logout_user, fresh_login_required
from app import db
from sqlalchemy import and_, or_
from app.models import User, Referral, Source
from app.referrals.forms import ReferralForm
from app.utils import send_new_referral_email, send_completed_referral_email

referrals = Blueprint('referrals', __name__)

# list of referral by source 
# list all referral for admin
@referrals.route("/referral/list")
@fresh_login_required
def list_referrals():
    user = User.query.get(current_user.id)
    if user.role == 'source':
        referrals = Referral.query.filter(and_(Referral.referral_status != 'complete', Referral.source_id == user.source_id)).all()
        return render_template('referrals/referral_list.html', title="Referrals", referrals=referrals)
    elif user.role == 'admin':      
        referrals = Referral.query.filter(Referral.referral_status != 'complete').all()
        return render_template('referrals/referral_list.html', title="Referrals", referrals=referrals)
    else:
        abort(403)


@referrals.route("/referral/new", methods=['GET', 'POST'])
@fresh_login_required
def new_referral():
    form = ReferralForm()
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        referral = Referral(firstname=form.firstname.data, lastname=form.lastname.data
                           , phone=form.phone.data, email=form.email.data, dob=form.dob.data
                           , poa_address1=form.poa_address1.data
                           , city=form.city.data, state=form.state.data, zip_code=form.zip_code.data
                           , medicare=Referral.encrypt_data(form.medicare.data), secondary=Referral.encrypt_data(form.secondary.data), discharge_date=form.discharge_date.data
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
                           , source_id=user.source_id)
        db.session.add(referral)
        db.session.commit()
        referral = Referral.query.get(referral.id)
        send_new_referral_email(referral, user)
        flash('The Referral was submitted successfully.', 'success')
        return redirect(url_for('referrals.list_referrals'))
    return render_template('referrals/crud_referral.html', title='Create Referral', form=form)


@referrals.route("/referral/<int:referral_id>")
@fresh_login_required
def referral(referral_id):
    referral = Referral.query.get_or_404(referral_id)
    to_decrypt = Referral.query.filter_by(id=referral_id).with_entities(Referral.medicare,Referral.secondary).first()
    d_medicare = Referral.decrypt_data(to_decrypt.medicare)
    d_secondary = Referral.decrypt_data(to_decrypt.secondary)
    submitter = User.query.get(referral.user_id)
    user = User.query.get(current_user.id)
    if referral.source_id == current_user.source_id:
        return render_template('referrals/referral.html', title=f"{referral.firstname} {referral.lastname}", referral=referral, user=user, submitter=submitter, d_medicare=d_medicare, d_secondary=d_secondary)
    elif current_user.role == 'admin':
        return render_template('referrals/referral.html', title=f"{referral.firstname} {referral.lastname}", referral=referral, user=user, submitter=submitter, d_medicare=d_medicare, d_secondary=d_secondary)
    else:
        abort(403)

@referrals.route("/referral/<int:referral_id>/complete", methods=['POST'])
@fresh_login_required
def referral_complete(referral_id):
    referral = Referral.query.get_or_404(referral_id)
    user = User.query.get(current_user.id)
    if user.role == 'admin':
        referral = Referral.query.get_or_404(referral_id)
        user = User.query.get(referral.user_id)

        send_completed_referral_email(referral, user)

        referral.referral_status = 'complete'
        db.session.commit()

        flash('The Referral has been completed. ', 'success')
    return redirect(url_for('main.home'))
    

@referrals.route("/referral/<int:referral_id>/delete", methods=['POST'])
@fresh_login_required
def delete_referral(referral_id):
    referral = Referral.query.get_or_404(referral_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(referral)
    db.session.commit()
    flash('The Referral was deleted successfully.', 'success')
    return redirect(url_for('main.home'))


@referrals.route("/referral/<int:referral_id>/update", methods=['GET', 'POST'])
@fresh_login_required
def update_referral(referral_id):
    referral = Referral.query.get_or_404(referral_id)
    user = User.query.get(current_user.id)
    if referral.source_id != user.source_id and current_user.role != 'admin':
        abort(403)
    form = ReferralForm()
    if form.validate_on_submit():
        referral.firstname=form.firstname.data
        referral.lastname=form.lastname.data
        referral.phone=form.phone.data
        referral.email=form.email.data
        referral.dob=form.dob.data
        referral.poa_address1=form.poa_address1.data
        referral.city=form.city.data
        referral.state=form.state.data
        referral.zip_code=form.zip_code.data
        referral.medicare=Referral.encrypt_data(form.medicare.data)
        referral.secondary=Referral.encrypt_data(form.secondary.data)
        referral.discharge_date=form.discharge_date.data
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
        return redirect(url_for('referrals.referral',referral_id=referral_id))
    elif request.method == 'GET':
        form.firstname.data=referral.firstname
        form.lastname.data=referral.lastname
        form.phone.data=referral.phone
        form.email.data=referral.email
        form.dob.data=referral.dob
        form.poa_address1.data=referral.poa_address1
        form.city.data=referral.city
        form.state.data=referral.state
        form.zip_code.data=referral.zip_code
        form.medicare.data=Referral.decrypt_data(referral.medicare)
        form.secondary.data=Referral.decrypt_data(referral.secondary)
        form.discharge_date.data=referral.discharge_date
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
    return render_template('referrals/crud_referral.html', title='Update Referral', form=form)