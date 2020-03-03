from app import app
from app.sources.routes import sources
from app.main.routes import main
from app.referrals.routes import referrals
from app.users.routes import users
from app.errors.handlers import errors

app.register_blueprint(sources)
app.register_blueprint(main)
app.register_blueprint(referrals)
app.register_blueprint(users)
app.register_blueprint(errors)


if __name__ == '__main__':
    app.run(debug=True)