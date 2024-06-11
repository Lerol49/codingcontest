from flask import Blueprint, render_template, redirect
from flask_login import logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .form import RegistrationForm, LoginForm
from .models import User, Team, create_new_team, create_new_user



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
        if User.query.filter_by(username=form.username.data).first() is not None:
            return '<h1>User already exists</h1>'
        hashed_password = generate_password_hash(form.password.data)

        new_user = create_new_user(username=form.username.data, password=hashed_password)
        new_user.give_access_to_contest("test_contest")

        if new_user.username == "max":
            create_new_team(new_user, "team1", "test_contest")
        else:
            Team.query.filter_by(name="team1").first().add_member(new_user)

        return redirect("/home")

    return render_template("signup.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect("home")



