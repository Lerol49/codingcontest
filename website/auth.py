from flask import Blueprint, render_template, redirect, flash
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
                flash("successfully logged in!")
                return redirect("home")

        flash("invalid username or password", "error")
    return render_template('login.html', form=form)



@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    if form.is_submitted():
        if not form.validate():
            flash("username and password have to have at least 3 characters", "error")
        else:
            if User.query.filter_by(username=form.username.data).first() is not None:
                flash("user already exists", "error")
            else:
                hashed_password = generate_password_hash(form.password.data)

                new_user = models.create_new_user(username=form.username.data, password=hashed_password)
                new_user.give_access_to_contest("the_beginning")

                return redirect("/home")

    return render_template("signup.html", form=form)


def create_team(contest_id):
    if current_user.get_team(contest_id) is not None:
        return redirect("https://www.youtube.com/watch?v=HIcSWuKMwOw")
    form = CreateTeam()
    if form.is_submitted():
        if not form.validate():
            flash("team_creation_error: teamname and password have to have at least 3 characters", "error")
        else:
            password = generate_password_hash(form.new_password.data)
            if Team.query.filter_by(name=form.new_teamname.data, contest_id=contest_id).first() is None:
                models.create_new_team(current_user, form.new_teamname.data, contest_id, password)
                flash("you successfully created the team " + form.new_teamname.data + "!")
            else:
                flash("team_creation_error: team already exists", "error")


def join_team(contest_id):
    form = JoinTeam()
    if form.is_submitted():
        if not form.validate():
            flash("team_join_error: teamname and password have to have at least 3 characters", "error")
        else:
            team = Team.query.filter_by(name=form.teamname.data, contest_id=contest_id).first()
            if team is not None and check_password_hash(team.password, form.password.data):
                if len(team.get_members()) < contest_data["contests"][contest_id]["team_size"]:
                    team.add_member(current_user)
                    flash("successfully joined team")
                else:
                    flash("team_join_error: the team is full", "error")
            else:
                flash("team_join_error: team doesn't exists or password is wrong", "error")



@auth.route("/logout")
def logout():
    logout_user()
    flash("successfully logged out!")
    return redirect("home")



