from functools import wraps
from flask import render_template, redirect, Blueprint, request, url_for, current_app, flash
from sqlalchemy.sql.functions import current_user
from flask_login import login_required, current_user
from . import auth
from .models import get_teams, get_contest
from .leaderboard import sort_teams_score
from . import form
from . import contest_data
from .models import Contest, init_Contests, User
from .other_requests import set_end_time
from werkzeug.security import check_password_hash, generate_password_hash
from .form import ChangeUsernameForm, ChangePasswordForm
from . import db

from .contest.contest_handling import handle_task_submission

views = Blueprint("views", __name__)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect("/login")

        if not current_user.rights == "admin":
            return redirect("https://www.youtube.com/watch?v=HIcSWuKMwOw")

        try:
            # current_app.ensure_sync available in Flask >= 2.0
            return current_app.ensure_sync(func)(*args, **kwargs)
        except AttributeError:  # pragma: no cover
            return func(*args, **kwargs)
    return wrapper


@views.route("/")
def page_0():
    return redirect(request.url + "home")

@views.route("/home")
def home():
    return render_template("/home.html", user=current_user)



# @views.route("/test_contest", methods=["POST", "GET"])
# @login_required
# def test_contest():
#     if request.method == "POST":
#         if "new_teamname" in request.form:
#             auth.create_team()
#         else:
#             auth.join_team()
#
#     return render_template("/test_contest/test_contest_index.html",
#                            user=current_user,
#                            team=current_user.get_team("test_contest"),
#                            problems=contest_data["contests"]["test_contest"]["problems"],
#                            teams=sort_teams_score("test_contest"))


@views.route("/contest/<contest_id>", methods=["POST", "GET"])
@login_required
def contest_index(contest_id):

    if request.method == "POST":
        if "new_teamname" in request.form:
            auth.create_team(contest_id)
        else:
            auth.join_team(contest_id)

    return render_template("/contest_index.html",
                           user=current_user,
                           team=current_user.get_team(contest_id),
                           contest_id=contest_id,
                           contest_name=contest_data["contests"][contest_id]["name"],
                           problems=contest_data["contests"][contest_id]["problems"],
                           teams=sort_teams_score(contest_id),
                           contest_stats=get_contest(contest_id).stats,
                           create_form=form.CreateTeam(),
                           join_form=form.JoinTeam())


@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    change_username_form = ChangeUsernameForm()
    change_password_form = ChangePasswordForm()

    if change_username_form.validate_on_submit():
        new_username = change_username_form.new_username.data
        if User.query.filter_by(username=new_username).first():
            flash("Username already exists.", "error")
        else:
            current_user.username = new_username
            db.session.commit()
            flash("Username changed successfully!", "success")
            return redirect(url_for("views.profile"))

    if change_password_form.validate_on_submit():
        if not check_password_hash(current_user.password, change_password_form.current_password.data):
            flash("Current password is incorrect.", "error")
        else:
            new_password = generate_password_hash(change_password_form.new_password.data)
            current_user.password = new_password
            db.session.commit()
            flash("Password changed successfully!", "success")
            return redirect(url_for("views.profile"))

    return render_template("profile.html", user=current_user, contests=contest_data["contests"],
                           change_username_form=change_username_form, change_password_form=change_password_form)




@views.route("contest/<contest_id>/<problem_id>", methods=["POST", "GET"])
@login_required
def load_contest_problem(contest_id, problem_id):
    if not Contest.query.filter_by(contest_id=contest_id).first().get_running() and current_user.rights != "admin":
        flash("Contest not running")
        return redirect("/contest/" + contest_id)

    if contest_data["contests"].get(contest_id) is None:
        return "no"

    if contest_data["contests"][contest_id]["problems"].get(problem_id.replace(".md", "")) is None:
        return "nein"

    handle_task_submission(contest_id, problem_id, "solutions/" + problem_id + "/output.txt")

    with open("website/templates/" + contest_id + "/" + problem_id + ".md", "r") as problem_file:
        markdown_text = problem_file.read()


    submission_type = contest_data["contests"][contest_id]["problems"][problem_id]["submission_type"]

    return render_template("/base_problem_md.html", problem_id=problem_id, problem_content=markdown_text,
                           user=current_user, submission_type=submission_type,
                           number_submission_form=form.NumberSubmission(),
                           contest_id=contest_id)



@views.route("/admin")
@admin_required
def load_admin_main():
    return render_template("/admin_main.html", contests=contest_data["contests"], user=current_user)


@views.route("/admin/<contest>", methods=["POST", "GET"])
@admin_required
def load_admin_contest(contest):
    """loading admin config page for specific contest"""
    if contest_data["contests"].get(contest) is None:
        return "no"

    set_end_time(contest)

    return render_template("/admin_contest_config.html", user=current_user,
                           problems=contest_data["contests"][contest]["problems"],
                           teams=get_teams(contest),
                           set_end_time_form=form.SetEndTime())











