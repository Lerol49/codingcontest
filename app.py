from flask import Flask, Blueprint, render_template, request, redirect, send_from_directory
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
from sqlalchemy.orm import attributes


private = True

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=15)])
    remember = BooleanField('Remember me')


class RegisterationForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=15)])



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


class Problems(db.Model):
    username = db.Column(db.String(15), unique=True, primary_key=True)
    pizza_distribution_problem = db.Column(db.JSON, default={"passed": False, "tries": 0})


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def page_0():
    return redirect(request.url + "home")


@app.route("/home")
def home():
    return render_template("/home.html", login_info=login_info())


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect("home")
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

    return render_template("signup.html", form=form)

def handle_task_submission(control_file, problem_name):
    # checks if user has already submitted someting
    user = Problems.query.filter_by(username=current_user.username).first()
    if user is None:
        new_try = Problems(username=current_user.username)
        db.session.add(new_try)
        db.session.commit()
        return ""

    elif request.method == "POST":
        submit_file = request.files["file"]
        if submit_file:
            submit_filename = secure_filename(submit_file.filename)
            submit_filepath = os.path.join(app.config["UPLOAD_DIRECTORY"], submit_filename)
            submit_file.save(submit_filepath)
            correct = compare_output_file(submit_filepath, control_file)
            user = Problems.query.filter_by(username=current_user.username).first()
            current_data = getattr(user, problem_name)
            if correct:
                current_data["passed"] = 1
                current_data["tries"] += 1
                setattr(user, problem_name, current_data)
                attributes.flag_modified(user, problem_name)
                db.session.commit()
                return "richtig!"
            else:
                current_data = getattr(user, problem_name)
                current_data["passed"] = 0
                current_data["tries"] += 1
                setattr(user, problem_name, current_data)
                attributes.flag_modified(user, problem_name)
                db.session.commit()
                return "falsch!"

    elif getattr(user, problem_name).get("tries") == 0:
        return ""

    else:
        problem = Problems.query.filter_by(username=current_user.username).first()
        if getattr(problem, problem_name).get("passed"):
            return "richtig"
        else:
            return "falsch"

    return ""



@app.route("/upload", methods=["POST", "GET"])
def test_upload_file():
    return render_template("upload.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("home")

def login_info():
    if current_user.is_authenticated:
        return "<div>" + current_user.username + "<a href='/logout'>&#160&#160&#160logout</a></div>"
    else:
        return "<div><a href='login'>login</a>&#160&#160&#160 <a href='/signup'>registrieren</a></div>"

@app.route("/test_contest")
@login_required
def test_contest():
    return render_template("/test_contest/test_contest_index.html", login_info=login_info())

@app.route("/test_contest/pizza_distribution_problem", methods=["POST", "GET"])
@login_required
def pizza_distribution_problem():
    result = handle_task_submission("solutions/pizza_distribution_problem/output.txt", "pizza_distribution_problem")
    return render_template("/test_contest/pizza_distribution_problem.html", result=result)
@app.route("/test_contest/pizza_distribution_problem/input.txt")
def pizza_distribution_problem_download_input():
    return send_from_directory("solutions/pizza_distribution_problem/", "input.txt")

def reset_test_values():
    pass


if __name__ == "__main__":
    # with app.app_context():
    #    db.create_all()
    app.run(host=ip, port=8000, debug=True)


