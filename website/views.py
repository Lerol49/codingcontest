from functools import wraps
from flask import render_template, redirect, Blueprint, request, send_from_directory, current_app, flash
from flask_login import login_required
from flask_login import current_user
from . import auth
from .models import get_teams, get_contest
from .leaderboard import sort_teams_score
from . import form
from . import contest_data
from .models import Contest, init_Contests

from .contest.contest_handling import handle_task_submission

views = Blueprint("views", __name__)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect("/login")

        if not current_user.rights == "admin":
            return "NICHT ADMIN"

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





@views.route("/profile")
@login_required
def profile():
    return render_template("/profile.html", user=current_user, contests=contest_data["contests"])




@views.route("contest/<contest_id>/<problem_id>", methods=["POST", "GET"])
@login_required
def load_contest_problem(contest_id, problem_id):
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
                           number_submission_form=form.NumberSubmission())



@views.route("/admin")
@admin_required
def load_admin_main():
    return render_template("/admin_main.html", contests=contest_data["contests"], user=current_user)


@views.route("/admin/<contest>")
@admin_required
def load_admin_contest(contest):
    """loading admin config page for specific contest"""
    if contest_data["contests"].get(contest) is None:
        return "no"
    return render_template("/admin_contest_config.html", user=current_user,
                           problems=contest_data["contests"][contest]["problems"],
                           teams=get_teams(contest))











