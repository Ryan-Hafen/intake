from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, fresh_login_required
from srs_intake import db
from srs_intake.models import Facility, User, Referral
from srs_intake.facilities.forms import FacilityForm


facilities = Blueprint('facilities', __name__)


@facilities.route("/facility/list")
@fresh_login_required
def list_facilities():
    user = User.query.get(current_user.id)
    if user.role == 'admin':
        facilities = Facility.query.all()
        return render_template('facilities/facilities_list.html', title="Facilities", facilities=facilities)
    else:
        abort(403)


@facilities.route("/facility/new", methods=['GET', 'POST'])
@fresh_login_required
def new_facility():
    form = FacilityForm()
    if form.validate_on_submit():
        facility = Facility(name=form.name.data,address1=form.address1.data, address2=form.address2.data, city=form.city.data, state=form.state.data, zip_code=form.zip_code.data, source=form.source.data)
        db.session.add(facility)
        db.session.commit()
        flash('The Facility was created successfully.', 'success')
        return redirect(url_for('main.home'))
    return render_template('facilities/crud_facility.html', title='Create Facility', form=form)


@facilities.route("/facility/<int:facility_id>")
@fresh_login_required
def facility(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    return render_template('facilities/facility.html', title=f"{facility.name}", facility=facility)


@facilities.route("/facility/<int:facility_id>/update", methods=['GET', 'POST'])
@fresh_login_required
def update_facility(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    if current_user.role != 'admin':
         abort(403)
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
        return redirect(url_for('facilities.facility',facility_id=facility_id))
    elif request.method == 'GET':
        form.name.data=facility.name
        form.address1.data=facility.address1
        form.address2.data=facility.address2
        form.city.data=facility.city
        form.state.data=facility.state
        form.zip_code.data=facility.zip_code
        form.source.data=facility.source
    return render_template('facilities/crud_facility.html', title='Update Facility', form=form)

@facilities.route("/facility/<int:facility_id>/delete", methods=['POST'])
@fresh_login_required
def delete_facility(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(facility)
    db.session.commit()
    flash('The Facility was deleted successfully.', 'success')
    return redirect(url_for('main.home'))