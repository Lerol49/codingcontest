from flask import Blueprint, render_template, redirect
from flask import current_app as app
from flask_login import current_user, logout_user, login_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .form import RegistrationForm, LoginForm
from .models import User


def login_info():
    if current_user.is_authenticated:
        return "<div> <a href='profile' >" + current_user.username + "<a/> <a href='/logout'>&#160&#160&#160logout</a></div>"
    else:
        return "<div><a href='login'>login</a>&#160&#160&#160 <a href='/signup'>registrieren</a></div>"


auth = Blueprint("auth", __name__)




@auth.route("/login", methods=["GET", "POST"])
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



@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/home")

    return render_template("signup.html", form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect("home")
