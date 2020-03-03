from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, fresh_login_required
from app import db
from app.models import Source, User, Referral
from app.sources.forms import SourceForm


sources = Blueprint('sources', __name__)


@sources.route("/sources/list")
@fresh_login_required
def list_source():
    user = User.query.get(current_user.id)
    if user.role == 'admin':
        sources = Source.query.all()
        return render_template('sources/source_list.html', title="Source", sources=sources)
    else:
        abort(403)


@sources.route("/sources/new", methods=['GET', 'POST'])
@fresh_login_required
def new_source():
    form = SourceForm()
    if form.validate_on_submit():
        source = Source(name=form.name.data,address1=form.address1.data, address2=form.address2.data, city=form.city.data, state=form.state.data, zip_code=form.zip_code.data, source=form.source.data)
        db.session.add(source)
        db.session.commit()
        flash('The Source was created successfully.', 'success')
        return redirect(url_for('main.home'))
    return render_template('sources/crud_source.html', title='Create Source', form=form)


@sources.route("/sources/<int:source_id>")
@fresh_login_required
def source(source_id):
    source = Source.query.get_or_404(source_id)
    return render_template('sources/source.html', title=f"{source.name}", source=source)


@sources.route("/sources/<int:source_id>/update", methods=['GET', 'POST'])
@fresh_login_required
def update_source(source_id):
    source = Source.query.get_or_404(source_id)
    if current_user.role != 'admin':
         abort(403)
    form = SourceForm()
    if form.validate_on_submit():
        source.name=form.name.data
        source.address1=form.address1.data
        source.address2=form.address2.data
        source.city=form.city.data
        source.state=form.state.data
        source.zip_code=form.zip_code.data
        source.source=form.source.data
        db.session.commit()
        flash('The Source was updated successfully.', 'success')
        return redirect(url_for('sources.source',source_id=source_id))
    elif request.method == 'GET':
        form.name.data=source.name
        form.address1.data=source.address1
        form.address2.data=source.address2
        form.city.data=source.city
        form.state.data=source.state
        form.zip_code.data=source.zip_code
        form.source.data=source.source
    return render_template('sources/crud_source.html', title='Update Source', form=form)

@sources.route("/sources/<int:source_id>/delete", methods=['POST'])
@fresh_login_required
def delete_source(source_id):
    source = Source.query.get_or_404(source_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(source)
    db.session.commit()
    flash('The Source was deleted successfully.', 'success')
    return redirect(url_for('main.home'))