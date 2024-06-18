from flask import Blueprint, render_template, redirect
from flask_login import logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .form import RegistrationForm, LoginForm, CreateTeam, JoinTeam
from .models import User, Team
from . import models, contest_data


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
        return "<h1>Invalid username or password</h1>"
    return render_template('login.html', form=form)



@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is not None:
            return '<h1>User already exists</h1>'
        hashed_password = generate_password_hash(form.password.data)

        new_user = models.create_new_user(username=form.username.data, password=hashed_password)
        new_user.give_access_to_contest("the_beginning")

        # if new_user.username == "max":
        #     create_new_team(new_user, "team1", "test_contest", "aaaa")
        # else:
        #     Team.query.filter_by(name="team1").first().add_member(new_user)

        return redirect("/home")

    return render_template("signup.html", form=form)


def create_team(contest_id):
    form = CreateTeam()
    password = generate_password_hash(form.password.data)
    if Team.query.filter_by(name=form.new_teamname.data, contest_id=contest_id).first() is None:
        models.create_new_team(current_user, form.new_teamname.data, contest_id, password)
    else:
        print("hi")
        return False  # irgendwie eine Fehlermeldung displayen


def join_team(contest_id):
    form = JoinTeam()
    team = Team.query.filter_by(name=form.teamname.data, contest_id=contest_id).first()
    if team is not None and check_password_hash(team.password, form.password.data):
        if len(team.get_members()) < contest_data["contests"][contest_id]["team_size"]:
            team.add_member(current_user)



@auth.route("/logout")
def logout():
    logout_user()
    return redirect("home")



