from srs_intake import app
from srs_intake.facilities.routes import facilities
from srs_intake.main.routes import main
from srs_intake.referrals.routes import referrals
from srs_intake.users.routes import users
from srs_intake.errors.handlers import errors

app.register_blueprint(facilities)
app.register_blueprint(main)
app.register_blueprint(referrals)
app.register_blueprint(users)
app.register_blueprint(errors)


if __name__ == '__main__':
    app.run(debug=True)