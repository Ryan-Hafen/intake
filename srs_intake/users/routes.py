
from flask import render_template, url_for, flash, redirect, request, abort, session, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from srs_intake import db, bcrypt
from srs_intake.models import User, Referral, Facility
from srs_intake.users.forms import RegistrationForm, LoginForm, UserForm, RequestResetForm, ResetPasswordForm
from srs_intake.utils import send_reset_email

users = Blueprint('users', __name__)




@users.route("/user/new", methods=['GET', 'POST'])
@login_required
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data,lastname=form.lastname.data, email=form.email.data, phone=form.phone.data, fax=form.fax.data, role=form.role.data, facility_id=form.facility_id.data, username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('The User was created successfully.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/create_user.html', title='Create User', form=form)


@users.route("/user/<int:user_id>")
@login_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/user.html', title=f"{user.firstname} {user.lastname}", user=user)


@users.route("/user/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if referral.facility_id != current_user.facility_id or current_user.role != 'admin':
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('The User was deleted successfully.', 'success')
    return redirect(url_for('main.home'))


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            # if not is_safe_url(next):
            #     return flask.abort(400)
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
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
        user = User.query.filter_by(username=form.username.data).first()
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


# @users.route("/account", methods=['GET', 'POST'])
# @login_required
# def account():
#     form = AccountForm()
#     if form.validate_on_submit():
#         current_user.firstname = form.firstname.data
#         current_user.lastname = form.lastname.data
#         current_user.email = form.email.data
#         current_user.phone = form.phone.data
#         current_user.fax = form.fax.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Your account has been updated!', 'success')
#         return redirect(url_for('users.account'))
#     elif request.method == 'GET':
#         form.firstname.data=current_user.firstname
#         form.lastname.data=current_user.lastname
#         form.email.data=current_user.email
#         form.phone.data=current_user.phone
#         form.fax.data=current_user.fax
#         form.email.data=current_user.email
#     return render_template('users/account.html', title='Update Account', form=form)


# @users.route("/user/<int:user_id>/update", methods=['GET', 'POST'])
# # @login_required
# def update_user(user_id):
#     user = User.query.get_or_404(user_id)
#     # if referral.facility_id != current_user.facility_id or current_user.role != 'admin':
#     #     abort(403)
#     form = UserForm()
#     if form.validate_on_submit():
#         current_user.firstname = form.firstname.data
#         current_user.lastname = form.lastname.data
#         current_user.phone = form.phone.data
#         current_user.fax = form.fax.data
#         db.session.commit()
#         flash('The User was updated successfully.', 'success')
#         return redirect(url_for('users.user',user_id=user_id))
#     elif request.method == 'GET':
#         form.firstname.data=current_user.firstname
#         form.lastname.data=current_user.lastname
#         form.phone.data=current_user.phone
#         form.fax.data=current_user.fax
#     return render_template('users/update_user.html', title='Update User', form=form)

# @users.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(firstname=form.firstname.data,lastname=form.lastname.data, email=form.email.data, phone=form.phone.data, fax=form.fax.data, role=form.role.data, facility_id=form.facility_id.data, username=form.username.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('users.login'))
#     return render_template('users/register.html', title='Register', form=form)