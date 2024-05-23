from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import secrets
import json

db = SQLAlchemy()
with (open("website/contest/contest.json", "r")) as contest:
    contest_data = json.load(contest)

def create_app():
    app = Flask(__name__, template_folder="templates")

    # Configure the Flask app
    app.config["UPLOAD_DIRECTORY"] = "uploads/"
    app.config["MAX_CONTENT_LENGTH"] = 400 * 1024  # 400KB
    app.config["SECRET_KEY"] = secrets.token_hex(16)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    # Initialize extensions
    db.init_app(app)
    Bootstrap(app)

    # Import and register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()

    from .models import User

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app
