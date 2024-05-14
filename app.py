from flask import Flask, Blueprint, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import socket
from compare_output_file import compare_output_file
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from wtforms import StringField, PasswordField, BooleanField
from flask_bootstrap import Bootstrap


private = True

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=10)])
    remember = BooleanField('Remember me')


class RegisterationForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=15)])



def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


if private:
    ip = "127.0.0.1"
else:
    ip = get_ip_address()

app = Flask(__name__)



# app.register_blueprint(views, url_prefix="/")
app.config["UPLOAD_DIRECTORY"] = "uploads/"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB
app.config["SECRET_KEY"] = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def page_0():
    return redirect(request.url + "home")


@app.route("/home")
def home():
    return render_template("/home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return "login successfull yeeee"
            return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return "<h1> New user has been created </h1>"

    return render_template("signup.html", form=form)



@app.route("/upload", methods=["POST", "GET"])
def upload_file():
    if request.method == "POST":
        submit_file = request.files["file"]
        if submit_file:
            submit_filename = secure_filename(submit_file.filename)
            submit_filepath = os.path.join(app.config["UPLOAD_DIRECTORY"], submit_filename)
            submit_file.save(submit_filepath)
            result = compare_output_file(submit_filepath, "templates/test_contest/cf_test_contest.txt")
            if result:
                return "yee"

    return render_template("upload.html")


@app.route("/test_contest")
def test_contest():
    return render_template("/test_contest/test_contest_index.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host=ip, port=8000, debug=True)

