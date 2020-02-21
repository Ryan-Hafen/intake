from flask import render_template, url_for, flash, redirect, request, jsonify
from srs_intake import app, db, bcrypt
from srs_intake.forms import RegistrationForm, LoginForm, CreateUserForm, CreateFacilityForm, UpdateAccountForm
from srs_intake.models import Facility, User, Referral
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    users = User.query.all()
    return render_template('home.html', users=users)

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


@app.route("/create_user", methods=['GET', 'POST'])
# @login_required
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data,lastname=form.lastname.data, email=form.email.data, phone=form.phone.data, fax=form.fax.data, role=form.role.data, facility_id=form.facility_id.data, username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('The User was created Successfully', 'success')
        return redirect(url_for('login'))
    return render_template('create_user.html', title='Create User', form=form)


@app.route("/create_facility", methods=['GET', 'POST'])
# @login_required
def create_facility():
    form = CreateFacilityForm()
    if form.validate_on_submit():
        facility = Facility(name=form.name.data,address1=form.address1.data, address2=form.address2.data, city=form.city.data, state=form.state.data, zip_code=form.zip_code.data, source=form.source.data)
        db.session.add(facility)
        db.session.commit()
        flash('The Facility was created Successfully', 'success')
        return redirect(url_for('login'))
    return render_template('create_facility.html', title='Create Facility', form=form)


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
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
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
    return render_template('account.html', title=f'Update {current_user.username}\'s account', form=form)