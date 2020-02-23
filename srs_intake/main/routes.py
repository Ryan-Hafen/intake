from flask import render_template, request, Blueprint
from srs_intake.models import Facility

main = Blueprint('main', __name__)



@main.route("/")
@main.route("/home")
def home():
    facilities = Facility.query.all()
    return render_template('home.html', facilities=facilities)
