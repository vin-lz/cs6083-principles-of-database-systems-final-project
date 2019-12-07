# ------------------------------------------------------------------------------
from flask import Flask
# ------------------------------------------------------------------------------
from flask_sqlalchemy import SQLAlchemy
# ------------------------------------------------------------------------------
from flask_login import LoginManager
# ------------------------------------------------------------------------------
import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'cloudsmile'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.debug = True
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Users

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Users.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    from .follow import follow as follow_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(follow_blueprint)

    return app
