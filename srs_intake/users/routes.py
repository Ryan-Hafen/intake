
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from srs_intake import db, bcrypt
from srs_intake.forms import RegistrationForm, LoginForm, UserForm, AccountForm, RequestResetForm, ResetPasswordForm
from srs_intake.models import User
from srs_intake.utils import send_reset_email

users = Blueprint('users', __name__)



@users.route("/register", methods=['GET', 'POST'])
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


@users.route("/user/new", methods=['GET', 'POST'])
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


@users.route("/user/<int:user_id>")
# @login_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', title=f"{user.firstname} {user.lastname}", user=user)


@users.route("/user/<int:user_id>/update", methods=['GET', 'POST'])
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


@users.route("/user/<int:user_id>/delete", methods=['POST'])
# @login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # if referral.facility_id != current_user.facility_id or current_user.role != 'admin':
    #     abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('The User was deleted successfully.', 'success')
    return redirect(url_for('home'))


@users.route("/login", methods=['GET', 'POST'])
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


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@users.route("/account", methods=['GET', 'POST'])
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

                
@users.route("/reset_password", methods=['GET', 'POST'])
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


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
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