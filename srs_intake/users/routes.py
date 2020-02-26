
from flask import render_template, url_for, flash, redirect, request, abort, session, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from srs_intake import app, db, bcrypt
from srs_intake.models import User, Referral, Facility
from srs_intake.users.forms import LoginForm, UserForm, UpdateUserForm, RequestResetForm, ResetPasswordForm
from srs_intake.utils import send_reset_email, send_new_account_email

users = Blueprint('users', __name__)


@users.route("/user/list")
@login_required
def list_users():
    user = User.query.get(current_user.id)
    if user.role == 'admin':      
        users = User.query.all()
        return render_template('users/users_list.html', title="Users", users=users)
    else:
        abort(403)


@users.route("/user/new", methods=['GET', 'POST'])
@login_required
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(app.config['SECRET_KEY']).decode('utf-8')
        user = User(firstname=form.firstname.data,lastname=form.lastname.data, email=form.email.data.lower(), phone=form.phone.data, fax=form.fax.data, role=form.role.data, facility_id=form.facility_id.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        send_new_account_email(user)
        flash('The User was created successfully.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/create_user.html', title='Create User', form=form)


@users.route("/user/<int:user_id>")
@login_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/user.html', title="User Info", user=user)


@users.route("/user/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.role != 'admin':
         abort(403)
    form = UpdateUserForm()
    if request.method == 'POST':
        user.firstname=form.firstname.data
        user.lastname=form.lastname.data
        user.email=form.email.data.lower()
        user.phone=form.phone.data
        user.fax=form.fax.data
        user.role=form.role.data
        user.facility_id=form.facility_id.data
        db.session.commit()
        flash('The User was updated successfully.', 'success')
        return redirect(url_for('users.user',user_id=user.id))
    elif request.method == 'GET':
        form.firstname.data=user.firstname
        form.lastname.data=user.lastname
        form.email.data=user.email
        form.phone.data=user.phone
        form.fax.data=user.fax
        form.role.data=user.role
        form.facility_id.data=user.facility_id
    return render_template('users/update_user.html', title='Update User', form=form)


@users.route("/user/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('The User was deleted successfully.', 'success')
    return redirect(url_for('users.list_users'))


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('users/login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

                
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html', title='Reset Password', form=form) 