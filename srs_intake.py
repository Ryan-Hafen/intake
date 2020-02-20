from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)



class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=True)
    address1 = db.Column(db.String(120), unique=True, nullable=True)
    address2 =db.Column(db.String(120), unique=True, nullable=True)
    city = db.Column(db.String(20), unique=True, nullable=True)
    state = db.Column(db.String(2), unique=True, nullable=True)
    zip_code = db.Column(db.String(10), unique=True, nullable=True)
    source = db.Column(db.String(10), unique=True, nullable=True)
    users = db.relationship('User', backref='user_loc', lazy=True)
    referals = db.relationship('Referral', backref='referral_loc', lazy=True)

    def __repr__(self):
        return f"Facility('{self.name}', '{self.city}', '{self.state}')"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=True, nullable=True)
    lastname = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    fax = db.Column(db.String(20), unique=True, nullable=True)
    role = db.Column(db.String(20), unique=True, nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=True)
    facility = db.relationship('Facility', backref='submitter', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', {self.role}', {self.firstname}', '{self.lastname}')"    


class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=True)
    lastname = db.Column(db.String(20), nullable=True)
    address1 = db.Column(db.String(120), nullable=True)
    address2 =db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(20), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    fax = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    ssn = db.Column(db.String(20), unique=True, nullable=True)
    medicare = db.Column(db.String(20), unique=True, nullable=True)
    secondary = db.Column(db.String(20), unique=True, nullable=True)
    discharge_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    notes = db.Column(db.String(255), nullable=True)
    disc_slp = db.Column(db.Boolean, nullable=True, default=False)
    disc_ot = db.Column(db.Boolean, nullable=True, default=False)
    disc_pt = db.Column(db.Boolean, nullable=True, default=False)
    treat_oral = db.Column(db.Boolean, nullable=True, default=False)
    treat_speech = db.Column(db.Boolean, nullable=True, default=False)
    treat_cognitive = db.Column(db.Boolean, nullable=True, default=False)
    treat_caregiver = db.Column(db.Boolean, nullable=True, default=False)
    treat_dementia = db.Column(db.Boolean, nullable=True, default=False)
    treat_adl = db.Column(db.Boolean, nullable=True, default=False)
    treat_safety = db.Column(db.Boolean, nullable=True, default=False)
    treat_upper_extremity = db.Column(db.Boolean, nullable=True, default=False)
    treat_ther_exercise = db.Column(db.Boolean, nullable=True, default=False)
    treat_balance = db.Column(db.Boolean, nullable=True, default=False)
    treat_ther_activity = db.Column(db.Boolean, nullable=True, default=False)
    treat_coordination = db.Column(db.Boolean, nullable=True, default=False)
    treat_transfer = db.Column(db.Boolean, nullable=True, default=False)
    treat_range = db.Column(db.Boolean, nullable=True, default=False)
    treat_massage = db.Column(db.Boolean, nullable=True, default=False)
    treat_pain = db.Column(db.Boolean, nullable=True, default=False)
    treat_wheelchair = db.Column(db.Boolean, nullable=True, default=False)
    treat_lower_extremity = db.Column(db.Boolean, nullable=True, default=False)
    treat_cane = db.Column(db.Boolean, nullable=True, default=False)
    treat_postural = db.Column(db.Boolean, nullable=True, default=False)
    treat_gait = db.Column(db.Boolean, nullable=True, default=False)
    treat_other = db.Column(db.Boolean, nullable=True, default=False)
    treat_other_desc = db.Column(db.String(120), nullable=True)
    med_firstname = db.Column(db.String(20), nullable=True)
    med_lastname = db.Column(db.String(20), nullable=True)
    med_address1 = db.Column(db.String(120), nullable=True)
    med_address2 =db.Column(db.String(120), nullable=True)
    med_city = db.Column(db.String(20), nullable=True)
    med_state = db.Column(db.String(2), nullable=True)
    med_zip_code = db.Column(db.String(10), nullable=True)
    med_email = db.Column(db.String(120), nullable=True)
    med_phone = db.Column(db.String(20), nullable=True)
    med_fax = db.Column(db.String(20), nullable=True)
    med_npi = db.Column(db.String(10), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=True)
    users = db.relationship('User', backref='user_ref', lazy=True)
    facility = db.relationship('Facility', backref='loc_ref', lazy=True)

    def __repr__(self):
        return f"Referral('{self.firstname}', '{self.lastname}', '{self.discharge_date}')" 


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
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)